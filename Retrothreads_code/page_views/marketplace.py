import streamlit as st
import pandas as pd
from utils.database import get_connection
from utils.components import page_header, condition_badge, section_divider
import mysql.connector

def render():
    conn   = get_connection()
    cursor = conn.cursor()

    # BUG FIX: Added INNER JOIN on approval table to only show 'Approved' items
    cursor.execute("""
        SELECT l.listing_id, l.garment_id, g.name AS garment_name,
               d.name AS designer,
               CONCAT(e.start_year, 's') AS era,
               g.`condition`, l.price, l.seller_id,
               l.status
        FROM listing l
        JOIN garment  g ON l.garment_id  = g.garment_id
        JOIN approval a ON g.garment_id  = a.entity_id 
                        AND a.entity_type = 'GARMENT' 
                        AND a.approval_status = 'Approved'
        LEFT JOIN designer d ON g.designer_id = d.designer_id
        LEFT JOIN era      e ON g.era_id      = e.era_id
    """)
    rows    = cursor.fetchall()
    columns = ["listing_id","garment_id","garment_name","designer",
               "era","condition","price","seller_id","status"]
    listings = pd.DataFrame(rows, columns=columns)

    page_header("Vintage Marketplace", "Authenticated Garments for Sale")

    if listings.empty:
        st.warning("No listings found in database.")
        return

    # ── Stats ──────────────────────────────────────────────────────────────────
    active = listings[listings["status"] == "active"]
    sold   = listings[listings["status"] == "sold"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{len(active)}</div>
            <div class="stat-label">Active Listings</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{len(sold)}</div>
            <div class="stat-label">Items Sold</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        avg_price = listings[listings["status"]=="active"]["price"].mean()
        avg_str   = f"${avg_price:,.0f}" if not pd.isna(avg_price) else "—"
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{avg_str}</div>
            <div class="stat-label">Avg. Active Price</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filters ────────────────────────────────────────────────────────────────
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">✦ Filter Listings</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        designers    = ["All"] + sorted([d for d in listings["designer"].unique() if pd.notna(d) and d])
        sel_designer = st.selectbox("Designer", designers, key="mp_designer")
    with fc2:
        eras    = ["All"] + sorted([e for e in listings["era"].unique() if pd.notna(e) and e])
        sel_era = st.selectbox("Era", eras, key="mp_era")
    with fc3:
        show_sold = st.checkbox("Show Sold Items", value=True, key="mp_show_sold")
    st.markdown('</div>', unsafe_allow_html=True)

    filtered = listings.copy()
    if sel_designer != "All":
        filtered = filtered[filtered["designer"] == sel_designer]
    if sel_era != "All":
        filtered = filtered[filtered["era"] == sel_era]
    if not show_sold:
        filtered = filtered[filtered["status"] != "sold"]

    st.markdown(f'<div style="color:var(--text-muted); font-size:0.8rem; letter-spacing:2px; margin-bottom:20px;">SHOWING {len(filtered)} LISTINGS</div>', unsafe_allow_html=True)

    if filtered.empty:
        st.markdown('<div style="text-align:center; padding:60px; color:var(--text-muted);">No listings match your filters.</div>', unsafe_allow_html=True)
        return

    # Using the real logged-in buyer ID from session state
    current_buyer_id = st.session_state.get("buyer_id", 1)

    cols_per_row = 3
    row_groups = [filtered.iloc[i:i+cols_per_row] for i in range(0, len(filtered), cols_per_row)]

    for row_df in row_groups:
        cols = st.columns(cols_per_row)
        for col, (_, listing) in zip(cols, row_df.iterrows()):
            with col:
                is_sold  = listing["status"] == "sold"
                price    = listing["price"] or 0

                # HTML strings kept flush left to prevent Streamlit code-block rendering
                sold_banner = """
<div style="position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(10,8,6,0.55); display:flex; align-items:center; justify-content:center; border-radius:6px 6px 0 0;">
<span style="background:#8a4a4a; color:#f0d0c8; font-family:'DM Mono',monospace; font-size:0.85rem; letter-spacing:3px; padding:6px 18px; border-radius:2px;">SOLD</span>
</div>""" if is_sold else ""

                st.markdown(f"""
<div class="garment-card" style="{'opacity:0.7;' if is_sold else ''}">
<div style="position:relative; height:190px; display:flex; align-items:center; justify-content:center; font-size:5rem; background:linear-gradient(135deg,#1a1714,#211e1a); border-radius:6px 6px 0 0;">
👗
{sold_banner}
</div>
<div class="garment-card-body">
<div class="garment-card-name">{listing['garment_name']}</div>
<div class="garment-card-meta">{listing['designer'] or '—'} · {listing['era'] or '—'}</div>
<div style="margin-top:6px;">{condition_badge(listing['condition'])}</div>
<div class="garment-card-price" style="font-size:1.3rem; margin-top:10px;">${float(price):,.0f}</div>
</div>
</div>
""", unsafe_allow_html=True)

                if not is_sold:
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("Buy Now", key=f"buy_{listing['listing_id']}", use_container_width=True):
                            try:
                                # 1. Start explicit transaction
                                cursor.execute("START TRANSACTION")
                                
                                # 2. Lock the specific listing row to prevent race conditions
                                cursor.execute("""
                                    SELECT status FROM listing 
                                    WHERE listing_id = %s FOR UPDATE
                                """, (int(listing["listing_id"]),))
                                
                                current_status = cursor.fetchone()[0]
                                
                                # 3. Check if someone else bought it a millisecond before us
                                if current_status != 'active':
                                    conn.rollback()
                                    st.error("Sorry, this item was just sold to another buyer!")
                                else:
                                    # 4. Process the purchase
                                    # (Note: we don't pass final_price because your set_transaction_price trigger handles it!)
                                    cursor.execute("""
                                        INSERT INTO transactions
                                            (listing_id, buyer_id, payment_status)
                                        VALUES (%s, %s, 'completed')
                                    """, (int(listing["listing_id"]), current_buyer_id))
                                    
                                    # 5. Commit the transaction (unlocks the row)
                                    conn.commit()
                                    st.success("✓ Purchase completed!")
                                    st.rerun()

                            except mysql.connector.Error as e:
                                # If any trigger fails (like prevent_self_purchase), undo everything
                                conn.rollback()
                                if "Fraud Prevention" in str(e) or "45000" in str(e):
                                    st.error("⚠️ You cannot purchase your own listing.")
                                else:
                                    st.error(f"Transaction failed: {e}")
                    with bc2:
                        if st.button("Details", key=f"det_{listing['listing_id']}", use_container_width=True):
                            st.session_state.selected_garment = int(listing["garment_id"])
                            st.session_state.page = "Museum"
                            st.rerun()
                else:
                    if st.button("View Archive →", key=f"arch_{listing['listing_id']}", use_container_width=True):
                        st.session_state.selected_garment = int(listing["garment_id"])
                        st.session_state.page = "Museum"
                        st.rerun()