import streamlit as st
import pandas as pd
from utils.database import get_connection

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            pe.event_id,
            g.name          AS garment,
            pe.event_name,
            pe.event_type,
            pe.event_date   AS date,
            pe.description,
            pe.location
        FROM provenance_event pe
        LEFT JOIN garment g ON pe.garment_id = g.garment_id
        ORDER BY pe.event_date ASC
    """)
    rows = cursor.fetchall()
    columns = ["event_id", "garment", "event_name", "event_type", "date", "description", "location"]
    df = pd.DataFrame(rows, columns=columns)
    df["date"] = pd.to_datetime(df["date"])
    return df

def render():
    # ── Custom CSS ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
        html, body, [class*="css"] { font-family: 'Georgia', serif; }

        .archive-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
            padding: 2.5rem 2rem 2rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        .archive-header h1 { color: #e8d5b0; font-size: 2.6rem; letter-spacing: 0.08em; margin: 0 0 0.25rem 0; font-weight: 700; }
        .archive-header p  { color: #a89070; font-size: 1rem; letter-spacing: 0.15em; text-transform: uppercase; margin: 0; }
        .stat-pill {
            display: inline-block; background: #e8d5b0; color: #1a1a2e;
            padding: 0.25rem 0.85rem; border-radius: 50px; font-size: 0.8rem;
            font-weight: 600; letter-spacing: 0.05em; margin-top: 1rem;
        }

        .event-card {
            background: #ffffff; border: 1px solid #e0d6c8;
            border-left: 5px solid #0f3460; border-radius: 8px;
            padding: 1.25rem 1.5rem; margin-bottom: 1.2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .event-card:hover { border-left-color: #e8a838; box-shadow: 0 4px 14px rgba(0,0,0,0.10); }
        .event-title { font-size: 1.15rem; font-weight: 700; color: #1a1a2e; margin: 0 0 0.5rem 0; }
        .event-meta  { display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.82rem; color: #666; margin-bottom: 0.75rem; }
        .event-desc  { font-size: 0.95rem; color: #333; line-height: 1.65; margin: 0; }

        .badge { display: inline-block; padding: 0.2rem 0.65rem; border-radius: 20px; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
        .badge-runway     { background: #fce8e8; color: #a32d2d; }
        .badge-museum     { background: #e6f1fb; color: #185fa5; }
        .badge-redcarpet  { background: #faeeda; color: #854f0b; }
        .badge-auction    { background: #eaf3de; color: #3b6d11; }
        .badge-private    { background: #f0eeff; color: #533ab7; }
        .badge-default    { background: #f1efe8; color: #5f5e5a; }

        .section-divider { display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0 1.2rem 0; }
        .section-divider span { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #0f3460; white-space: nowrap; }
        .section-divider hr   { flex: 1; border: none; border-top: 1px solid #e0d6c8; margin: 0; }

        .no-result { text-align: center; padding: 3rem 1rem; color: #999; font-size: 1rem; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

    try:
        events = load_events()
    except Exception as e:
        st.error(f"Database error: {e}")
        st.stop()

    # ── Header ─────────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="archive-header">
        <h1>🏛️ Cultural Archive</h1>
        <p>Provenance &amp; Heritage Records</p>
        <div class="stat-pill">
            {len(events)} record{"s" if len(events) != 1 else ""}
            &nbsp;·&nbsp;
            {events['garment'].nunique()} garment{"s" if events['garment'].nunique() != 1 else ""}
            &nbsp;·&nbsp;
            {events['event_type'].nunique()} categor{"ies" if events['event_type'].nunique() != 1 else "y"}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if events.empty:
        st.warning("No provenance records found in database.")
        st.stop()

    # ── Filters ────────────────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns([1, 1, 1])

    with fc1:
        types = ["All"] + sorted(events["event_type"].dropna().unique().tolist())
        sel_type = st.selectbox("Event Type", types)

    with fc2:
        garments = ["All"] + sorted(events["garment"].dropna().unique().tolist())
        sel_garment = st.selectbox("Related Garment", garments)

    with fc3:
        locations = ["All"] + sorted(events["location"].dropna().unique().tolist())
        sel_location = st.selectbox("Location", locations)

    # ── Apply Filters ──────────────────────────────────────────────────────────────
    filtered = events.copy()
    if sel_type     != "All": filtered = filtered[filtered["event_type"] == sel_type]
    if sel_garment  != "All": filtered = filtered[filtered["garment"]    == sel_garment]
    if sel_location != "All": filtered = filtered[filtered["location"]   == sel_location]
    filtered = filtered.sort_values("date").reset_index(drop=True)

    # ── Timeline ───────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="section-divider">
        <span>Event Timeline</span><hr>
        <span style="white-space:nowrap; color:#999; font-size:0.72rem;">
            {len(filtered)} result{"s" if len(filtered) != 1 else ""}
        </span>
    </div>
    """, unsafe_allow_html=True)

    if filtered.empty:
        st.markdown('<div class="no-result">No records match the selected filters.</div>', unsafe_allow_html=True)
    else:
        badge_map = {
            "Runway Show":       "badge-runway",
            "Museum Exhibition": "badge-museum",
            "Red Carpet":        "badge-redcarpet",
            "Auction":           "badge-auction",
            "Private Event":     "badge-private",
        }

        for _, ev in filtered.iterrows():
            badge_cls = badge_map.get(ev["event_type"], "badge-default")
            date_str  = ev["date"].strftime("%d %b %Y")
            garment   = ev["garment"] if pd.notna(ev["garment"]) else "Unknown Garment"

            st.markdown(f"""
            <div class="event-card">
                <p class="event-title">{ev['event_name']}</p>
                <div class="event-meta">
                    <span>🗓️ {date_str}</span>
                    <span>📍 {ev['location']}</span>
                    <span>🧥 {garment}</span>
                </div>
                <p class="event-desc">{ev['description']}</p>
                <div style="margin-top:0.75rem;">
                    <span class="badge {badge_cls}">{ev['event_type']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Footer ─────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#aaa; font-size:0.8rem; font-style:italic;'>"
        "RetroThreads Cultural Archive &nbsp;·&nbsp; Heritage & Provenance Records"
        "</p>",
        unsafe_allow_html=True,
    )
    