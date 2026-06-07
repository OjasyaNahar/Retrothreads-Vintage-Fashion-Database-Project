import streamlit as st
st.set_page_config(
    page_title="RetroThreads",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Safe imports with error display ──────────────────────────────────────────
try:
    from utils.styles import inject_global_styles
    inject_global_styles()
except Exception as e:
    st.error(f"styles.py error: {e}")

try:
    from page_views import home, museum, marketplace, cultural_archive, seller_dashboard, admin_panel
    from page_views.buyer_dashboard import render as buyer_render
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "selected_garment" not in st.session_state:
    st.session_state.selected_garment = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧵 RetroThreads")
    st.markdown("*Preserving Fashion History*")
    st.markdown("---")

    nav_items = {
        "🏠 Home":             "Home",
        "🏛️ Digital Museum":   "Museum",
        "📜 Cultural Archive": "Cultural Archive",
        "🛒 Marketplace":      "Marketplace",
        "🛍️ Buyer Dashboard":  "Buyer Dashboard",
        "📦 Seller Dashboard": "Seller Dashboard",
        "🔐 Admin Panel":      "Admin Panel",
    }

    for label, page_key in nav_items.items():
        if st.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.session_state.selected_garment = None
            st.rerun()

    st.markdown("---")
    st.caption("©️ 2025 RetroThreads · Group 30")

# ── Page routing ──────────────────────────────────────────────────────────────
page = st.session_state.page

try:
    if page == "Home":
        home.render()
    elif page == "Museum":
        museum.render()
    elif page == "Cultural Archive":
        cultural_archive.render()
    elif page == "Marketplace":
        marketplace.render()
    elif page == "Buyer Dashboard":
        buyer_render()
    elif page == "Seller Dashboard":
        seller_dashboard.render()
    elif page == "Admin Panel":
        admin_panel.render()
except Exception as e:
    st.error(f"Page render error on '{page}': {e}")
    st.exception(e)
