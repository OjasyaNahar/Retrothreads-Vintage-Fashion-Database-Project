import streamlit as st
import pandas as pd
from utils.database import get_connection
from utils.components import (
    page_header, garment_card_html, condition_badge,
    style_tags_html, section_divider, timeline_event
)


def render():
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.garment_id, g.name, d.name AS designer,
               CONCAT(e.start_year, 's') AS era,
               g.material, g.size, g.`condition`, g.description, g.image_reference
        FROM garment g
        LEFT JOIN designer d ON g.designer_id = d.designer_id
        LEFT JOIN era      e ON g.era_id      = e.era_id
    """)
    rows    = cursor.fetchall()
    columns = ["garment_id","name","designer","era","material","size","condition","description","icon"]
    garments = pd.DataFrame(rows, columns=columns)
    garments["icon"]           = "👗"
    garments["style_tags"]     = [[] for _ in range(len(garments))]
    garments["listing_status"] = "Available"
    garments["celebrity"]      = "—"

    if st.session_state.selected_garment is not None:
        _render_detail(garments, cursor)
        return

    page_header("Digital Museum", "Garment Archive")

    # ── Filters ────────────────────────────────────────────────────────────────
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">✦ Filter Collection</div>', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)

    # Added pd.notna() to safely handle missing data (NULL/NaN) before sorting
    designers  = ["All"] + sorted([d for d in garments["designer"].unique() if pd.notna(d) and d])
    eras       = ["All"] + sorted([e for e in garments["era"].unique()      if pd.notna(e) and e])
    materials  = ["All"] + sorted([m for m in garments["material"].unique() if pd.notna(m) and m])
    conditions = ["All", "Excellent", "Good", "Fair", "Poor"]

    with fc1: sel_designer  = st.selectbox("Designer",  designers,  key="m_designer")
    with fc2: sel_era       = st.selectbox("Era",       eras,       key="m_era")
    with fc3: sel_material  = st.selectbox("Material",  materials,  key="m_material")
    with fc4: sel_condition = st.selectbox("Condition", conditions, key="m_condition")
    st.markdown('</div>', unsafe_allow_html=True)

    filtered = garments.copy()
    if sel_designer  != "All": filtered = filtered[filtered["designer"]  == sel_designer]
    if sel_era       != "All": filtered = filtered[filtered["era"]       == sel_era]
    if sel_material  != "All": filtered = filtered[filtered["material"]  == sel_material]
    if sel_condition != "All": filtered = filtered[filtered["condition"] == sel_condition]

    st.markdown(f'<div style="color:var(--text-muted); font-size:0.8rem; letter-spacing:2px; margin-bottom:20px;">SHOWING {len(filtered)} GARMENTS</div>', unsafe_allow_html=True)

    if filtered.empty:
        st.markdown('<div style="text-align:center; padding:60px; color:var(--text-muted);">No garments match the selected filters.</div>', unsafe_allow_html=True)
        return

    cols_per_row = 4
    row_groups = [filtered.iloc[i:i+cols_per_row] for i in range(0, len(filtered), cols_per_row)]
    for row_df in row_groups:
        cols = st.columns(cols_per_row)
        for col, (_, garment) in zip(cols, row_df.iterrows()):
            with col:
                st.markdown(garment_card_html(garment.to_dict()), unsafe_allow_html=True)
                if st.button("View Details →", key=f"museum_view_{garment['garment_id']}", use_container_width=True):
                    st.session_state.selected_garment = int(garment["garment_id"])
                    st.rerun()


def _render_detail(garments, cursor):
    gid = st.session_state.selected_garment
    row = garments[garments["garment_id"] == gid]
    if row.empty:
        st.error("Garment not found.")
        return

    garment = row.iloc[0].to_dict()

    if st.button("← Back to Museum", key="back_museum"):
        st.session_state.selected_garment = None
        st.rerun()

    # ── TRIGGER 1: Live listing status ─────────────────────────────────────────
    cursor.execute("""
        SELECT status FROM listing
        WHERE garment_id = %s
        ORDER BY listing_id DESC LIMIT 1
    """, (gid,))
    listing_row = cursor.fetchone()
    live_status = listing_row[0].capitalize() if listing_row else "Not Listed"
    is_sold     = live_status.lower() == "sold"

    st.markdown(f"""
    <div style="margin: 24px 0 8px;">
        <div style="font-family:'Playfair Display',serif; font-size:2.4rem; color:var(--text-primary);">{garment['name']}</div>
        <div style="font-size:1rem; color:var(--accent-gold); letter-spacing:2px;">{garment['designer'] or '—'} · {garment['era'] or '—'}</div>
        <div class="gold-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col_img, col_info = st.columns([1, 2], gap="large")

    with col_img:
        sold_overlay = """
            <div style="position:absolute; top:12px; right:12px;
                background:#8a4a4a; color:#f0d0c8; font-family:'DM Mono',monospace;
                font-size:0.7rem; letter-spacing:2px; padding:4px 10px; border-radius:2px;">
                SOLD
            </div>""" if is_sold else ""

        st.markdown(f"""
        <div style="position:relative; background:linear-gradient(135deg,#1a1714,#211e1a);
             border:1px solid {'#8a4a4a' if is_sold else 'var(--border-accent)'};
             border-radius:8px; height:360px;
             display:flex; align-items:center; justify-content:center; font-size:8rem;
             {'opacity:0.6;' if is_sold else ''}">
            👗
            {sold_overlay}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:6px;"><span class="detail-label">Condition</span></div>
        <div>{condition_badge(garment['condition'])}</div>
        <div style="margin-top:14px;"><span class="detail-label">Listing Status</span></div>
        <div style="margin-top:4px;">
            <span class="badge {'badge-poor' if is_sold else 'badge-excellent'}">{live_status}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        section_divider("Overview")
        meta = [
            ("Designer",    garment.get("designer") or "—"),
            ("Fashion Era", garment.get("era")      or "—"),
            ("Material",    garment.get("material") or "—"),
            ("Size",        garment.get("size")     or "—"),
        ]
        mc1, mc2 = st.columns(2)
        for i, (lbl, val) in enumerate(meta):
            with (mc1 if i % 2 == 0 else mc2):
                st.markdown(f"""
                <div style="margin-bottom:16px;">
                    <div class="detail-label">{lbl}</div>
                    <div class="detail-value" style="margin-top:2px;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        section_divider("Description")
        st.markdown(f'<p style="line-height:1.8; font-size:1rem;">{garment.get("description") or "No description available."}</p>', unsafe_allow_html=True)

        section_divider("Authenticity Documents")
        for doc in ["Certificate of Authenticity (PDF)", "Original Purchase Receipt (Scanned)", "Curator Verification Note"]:
            st.markdown(f'<div style="padding:10px 14px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:4px; margin-bottom:8px; font-size:0.85rem; color:var(--text-secondary);">📄 {doc}</div>', unsafe_allow_html=True)

    # ── Provenance (if table exists) ───────────────────────────────────────────
    section_divider("Provenance History")
    try:
        cursor.execute("""
            SELECT date, event_name, description, event_type
            FROM provenance_events
            WHERE garment_id = %s
            ORDER BY date
        """, (gid,))
        prov_rows = cursor.fetchall()
        if prov_rows:
            for date, event_name, desc, etype in prov_rows:
                timeline_event(str(date), event_name, desc or "", etype or "")
        else:
            st.markdown('<p>No provenance records available.</p>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<p>No provenance records available.</p>', unsafe_allow_html=True)
