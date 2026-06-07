import streamlit as st
import hashlib
from utils.database import get_connection
from utils.components import page_header, section_divider


def render():
    page_header("Seller Dashboard", "List Your Vintage Garments")

    if "seller_logged_in" not in st.session_state:
        st.session_state.seller_logged_in = False

    if not st.session_state.seller_logged_in:
        _render_login()
        return

    _render_dashboard()


def _render_login():
    st.markdown("""
    <div style="max-width:420px; margin:40px auto;">
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:3rem;">🏷️</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.6rem; color:var(--text-primary); margin-top:8px;">Seller Portal</div>
            <div style="font-size:0.8rem; color:var(--text-muted); letter-spacing:2px; margin-top:4px;">VERIFIED SELLERS ONLY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        email    = st.text_input("Email", placeholder="seller@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign In to Dashboard", use_container_width=True):
            if email and password:
                conn   = get_connection()
                cursor = conn.cursor()

                # Look up user by email and role
                cursor.execute("""
                    SELECT user_id, name, role, password_hash
                    FROM users
                    WHERE email = %s AND role = 'seller'
                """, (email,))
                user_row = cursor.fetchone()

                if not user_row:
                    st.error("No seller account found with that email.")
                else:
                    user_id, name, role, stored_hash = user_row

                    # Hash the entered password the same way it was stored
                    # Tries plain MD5 first, then SHA256, then plaintext match
                    entered_md5    = hashlib.md5(password.encode()).hexdigest()
                    entered_sha256 = hashlib.sha256(password.encode()).hexdigest()

                    if password == stored_hash or entered_md5 == stored_hash or entered_sha256 == stored_hash:
                        st.session_state.seller_logged_in = True
                        st.session_state.seller_email     = email
                        st.session_state.seller_name      = name
                        st.session_state.seller_id        = user_id
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
            else:
                st.error("Please enter your email and password.")

        st.markdown("""
        <div style="text-align:center; font-size:0.75rem; color:var(--text-muted); margin-top:12px;">
            Use an email from the <code>users</code> table with role = 'seller'
        </div>
        """, unsafe_allow_html=True)


def _render_dashboard():
    email     = st.session_state.get("seller_email", "")
    name      = st.session_state.get("seller_name", "Seller")
    seller_id = st.session_state.get("seller_id")

    conn   = get_connection()
    cursor = conn.cursor()

    col_h, col_btn = st.columns([4, 1])
    with col_h:
        st.markdown(f"""
        <div style="margin-bottom:4px;">
            <span style="font-family:'Playfair Display',serif; font-size:1.1rem; color:var(--text-primary);">{name}</span>
            <span style="font-size:0.8rem; color:var(--text-muted); margin-left:8px;">{email}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        if st.button("Sign Out"):
            st.session_state.seller_logged_in = False
            st.session_state.seller_id        = None
            st.rerun()

    # ── My submissions + live approval status (TRIGGER 2 reflection) ───────────
    section_divider("My Submissions & Approval Status")
    st.markdown('<p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:16px;">Approval rows are created automatically by the <code>initialize_garment_approval</code> trigger the moment your garment is inserted.</p>', unsafe_allow_html=True)

    cursor.execute("""
        SELECT g.garment_id, g.name,
               CONCAT(e.start_year,'s') AS era,
               a.approval_status,
               l.price, l.status AS listing_status
        FROM listing l
        JOIN garment  g ON l.garment_id  = g.garment_id
        LEFT JOIN era      e ON g.era_id      = e.era_id
        LEFT JOIN approval a ON a.entity_id   = g.garment_id
                             AND a.entity_type = 'GARMENT'
        WHERE l.seller_id = %s
        ORDER BY g.garment_id DESC
    """, (seller_id,))
    my_rows = cursor.fetchall()

    if my_rows:
        for gid, gname, era, approval_status, price, lst_status in my_rows:
            approval_status = approval_status or "Pending"
            lst_status      = lst_status      or "—"
            price           = float(price)    if price else 0

            ap_class = {"Approved": "badge-excellent", "Rejected": "badge-poor", "Pending": "badge-good"}.get(approval_status, "badge-good")
            ls_class = "badge-poor" if lst_status == "sold" else "badge-excellent"

            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                 border-radius:6px; padding:16px 20px; margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                    <span style="font-size:2rem;">👗</span>
                    <div style="flex:1;">
                        <div style="font-family:'Playfair Display',serif; font-size:1rem; color:var(--text-primary);">{gname}</div>
                        <div style="font-size:0.8rem; color:var(--text-muted);">{era or '—'} · <span style="color:var(--accent-gold);">${price:,.0f}</span></div>
                    </div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap;">
                        <span class="badge {ap_class}">Approval: {approval_status}</span>
                        <span class="badge {ls_class}">Listing: {lst_status}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:var(--text-muted);">No submissions found for your account yet.</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Submit New Listing ─────────────────────────────────────────────────────
    section_divider("Submit New Listing")
    st.markdown('<p style="font-size:0.85rem; color:var(--text-muted);">All submissions are reviewed by our curatorial team. The <code>initialize_garment_approval</code> trigger automatically queues your garment for admin review on insert.</p>', unsafe_allow_html=True)

    # Load real designers and eras from DB for dropdowns
    cursor.execute("SELECT designer_id, name FROM designer ORDER BY name")
    designer_options = cursor.fetchall()

    cursor.execute("SELECT era_id, CONCAT(start_year,'s') FROM era ORDER BY start_year")
    era_options = cursor.fetchall()

    designer_map = {name: did for did, name in designer_options}
    era_map      = {label: eid for eid, label in era_options}

    if not designer_map:
        st.warning("No designers found in the database. Please add designers via the Admin Panel first.")
        return
    if not era_map:
        st.warning("No eras found in the database. Please add eras first.")
        return

    with st.form("new_listing_form"):
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            garment_name = st.text_input("Garment Name *",  placeholder="e.g. Dior New Look Suit")
            sel_designer = st.selectbox("Designer *",       list(designer_map.keys()))
            sel_era      = st.selectbox("Fashion Era *",    list(era_map.keys()))
        with r1c2:
            material  = st.text_input("Material *",  placeholder="e.g. Silk, Wool Crepe")
            size      = st.text_input("Size",         placeholder="e.g. FR 38, UK 10")
            condition = st.selectbox("Condition *",  ["Excellent", "Good", "Fair", "Poor"])

        description = st.text_area("Description *", placeholder="Describe the garment's history, design details, and provenance...", height=120)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            price = st.number_input("Asking Price (USD) *", min_value=0, value=1000, step=100)
        with r2c2:
            st.text_input("Style Tags", placeholder="e.g. Couture, Minimalist (comma separated)")

        dc1, dc2 = st.columns(2)
        with dc1:
            st.file_uploader("Certificate of Authenticity", type=["pdf", "jpg", "png"], key="cert")
        with dc2:
            st.file_uploader("Original Purchase Receipt",   type=["pdf", "jpg", "png"], key="receipt")

        st.file_uploader("Garment Image *", type=["jpg", "jpeg", "png", "webp"], key="garment_img")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit for Review", use_container_width=True)

        if submitted:
            if garment_name and description:
                try:
                    designer_id = designer_map[sel_designer]
                    era_id      = era_map[sel_era]

                    # INSERT garment → fires initialize_garment_approval trigger automatically
                    cursor.execute("""
                        INSERT INTO garment
                            (name, description, `condition`, size, material, designer_id, era_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (garment_name, description, condition, size or None, material, designer_id, era_id))
                    new_garment_id = cursor.lastrowid

                    # INSERT listing with the real seller_id from session
                    cursor.execute("""
                        INSERT INTO listing (garment_id, seller_id, price, status)
                        VALUES (%s, %s, %s, 'active')
                    """, (new_garment_id, seller_id, price))

                    conn.commit()
                    st.success(f"✓ '{garment_name}' submitted! It has been automatically queued for admin approval.")
                    st.rerun()

                except Exception as e:
                    conn.rollback()
                    st.error(f"Submission failed: {e}")
            else:
                st.error("Please fill in all required fields (marked with *).")