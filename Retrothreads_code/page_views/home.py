import streamlit as st
import pandas as pd
from utils.database import get_connection
from utils.components import stat_card, garment_card_html


def render():
    conn   = get_connection()
    cursor = conn.cursor()

    # JOIN garment → designer + era to get readable names
    cursor.execute("""
        SELECT g.garment_id, g.name, d.name AS designer,
               CONCAT(e.start_year, 's') AS era,
               g.material, g.`condition`, g.image_reference
        FROM garment g
        LEFT JOIN designer d ON g.designer_id = d.designer_id
        LEFT JOIN era      e ON g.era_id      = e.era_id
    """)
    rows    = cursor.fetchall()
    columns = ["garment_id","name","designer","era","material","condition","icon"]
    garments = pd.DataFrame(rows, columns=columns)
    garments["icon"]       = "👗"
    garments["style_tags"] = [[] for _ in range(len(garments))]

    # ── Hero ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-eyebrow">✦ Fashion Heritage Management System</div>
        <div class="hero-title">Retro<em>Threads</em></div>
        <div class="hero-body">
            A curated digital archive preserving the cultural memory of vintage fashion —
            from Dior's New Look to Westwood's punk revolution.
            Discover, research, and acquire authenticated pieces.
        </div>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <span class="tag tag-gold">Digital Archive</span>
            <span class="tag tag-gold">Authenticated Marketplace</span>
            <span class="tag tag-gold">Provenance Records</span>
            <span class="tag tag-gold">Cultural Heritage</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Live stats from DB ─────────────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM listing WHERE status = 'active'")
    active_listings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM designer")
    designer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM approval WHERE approval_status = 'Approved'")
    approved_count = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1: stat_card(len(garments),    "Archived Garments")
    with col2: stat_card(active_listings,  "Active Listings")
    with col3: stat_card(designer_count,   "Verified Designers")
    with col4: stat_card(approved_count,   "Approved Items")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Featured Garments ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:20px;">
        <div>
            <div class="page-title" style="font-size:1.8rem;">Featured Pieces</div>
            <div class="gold-line"></div>
        </div>
        <div class="hero-eyebrow">✦ Curated Selection</div>
    </div>
    """, unsafe_allow_html=True)

    featured = garments[garments["condition"] == "Excellent"].head(4)
    if featured.empty:
        featured = garments.head(4)

    cols = st.columns(4)
    for i, (_, row) in enumerate(featured.iterrows()):
        with cols[i % 4]:
            st.markdown(garment_card_html(row.to_dict()), unsafe_allow_html=True)
            if st.button("View Details", key=f"home_view_{row['garment_id']}", use_container_width=True):
                st.session_state.selected_garment = int(row["garment_id"])
                st.session_state.page = "Museum"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Links ────────────────────────────────────────────────────────────
    st.markdown('<div class="detail-section-title">Explore RetroThreads</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    quick_links = [
        ("🏛️", "Digital Museum",   "Browse archived garments with full provenance and cultural context.", "Museum"),
        ("📜", "Cultural Archive", "Explore provenance events — runway shows, exhibitions, celebrity moments.", "Cultural Archive"),
        ("🛒", "Marketplace",      "Buy authenticated vintage garments from verified global sellers.", "Marketplace"),
    ]
    for col, (icon, title, desc, page) in zip([c1, c2, c3], quick_links):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="text-align:left; padding:24px; min-height:140px;">
                <div style="font-size:2rem; margin-bottom:10px;">{icon}</div>
                <div style="font-family:'Playfair Display',serif; font-size:1.1rem; color:var(--text-primary); margin-bottom:6px;">{title}</div>
                <div style="font-size:0.85rem; color:var(--text-muted); line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go to {title}", key=f"ql_{title}", use_container_width=True):
                st.session_state.page = page
                st.rerun()