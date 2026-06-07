import streamlit as st
import hashlib
from utils.database import get_connection
from utils.components import page_header, section_divider

def render():
    page_header("Buyer Dashboard", "Manage Your Vintage Collection")

    if "buyer_logged_in" not in st.session_state:
        st.session_state.buyer_logged_in = False

    if not st.session_state.buyer_logged_in:
        _render_login()
        return

    _render_dashboard()

def _render_login():
    st.markdown("""
    <div style="max-width:420px; margin:40px auto;">
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:3rem;">🛍️</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.6rem; color:var(--text-primary); margin-top:8px;">Buyer Portal</div>
            <div style="font-size:0.8rem; color:var(--text-muted); letter-spacing:2px; margin-top:4px;">VERIFIED BUYERS ONLY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        email    = st.text_input("Email", placeholder="buyer@example.com")
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
                    WHERE email = %s AND role = 'buyer'
                """, (email,))
                user_row = cursor.fetchone()

                if not user_row:
                    st.error("No buyer account found with that email.")
                else:
                    user_id, name, role, stored_hash = user_row

                    # Handle password hashing matching your other panels
                    entered_md5    = hashlib.md5(password.encode()).hexdigest()
                    entered_sha256 = hashlib.sha256(password.encode()).hexdigest()

                    if password == stored_hash or entered_md5 == stored_hash or entered_sha256 == stored_hash:
                        st.session_state.buyer_logged_in = True
                        st.session_state.buyer_email     = email
                        st.session_state.buyer_name      = name
                        st.session_state.buyer_id        = user_id
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
            else:
                st.error("Please enter your email and password.")
                
        st.markdown("""
        <div style="text-align:center; font-size:0.75rem; color:var(--text-muted); margin-top:12px;">
            Use an email from the <code>users</code> table with role = 'buyer'
        </div>
        """, unsafe_allow_html=True)

def _render_dashboard():
    email    = st.session_state.get("buyer_email", "")
    name     = st.session_state.get("buyer_name", "Buyer")
    buyer_id = st.session_state.get("buyer_id")

    conn   = get_connection()
    cursor = conn.cursor()

    # -- User Info & Logout --
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
            st.session_state.buyer_logged_in = False
            st.session_state.buyer_id        = None
            st.rerun()

    section_divider("My Purchase History")

    # Fetch purchases tied to this specific buyer from the database
    cursor.execute("""
        SELECT t.transaction_id, t.payment_status,
               g.name AS garment_name,
               d.name AS designer,
               CONCAT(e.start_year, 's') AS era,
               l.price, g.garment_id
        FROM transactions t
        JOIN listing l ON t.listing_id = l.listing_id
        JOIN garment g ON l.garment_id = g.garment_id
        LEFT JOIN designer d ON g.designer_id = d.designer_id
        LEFT JOIN era e ON g.era_id = e.era_id
        WHERE t.buyer_id = %s
        ORDER BY t.transaction_id DESC
    """, (buyer_id,))
    purchases = cursor.fetchall()

    if not purchases:
        st.markdown('<p style="color:var(--text-muted); padding: 20px 0;">You haven\'t purchased any items yet. Your acquired pieces will appear here.</p>', unsafe_allow_html=True)
        if st.button("Browse Marketplace", use_container_width=False):
            st.session_state.page = "Marketplace"
            st.rerun()
    else:
        for tid, status, gname, designer, era, price, gid in purchases:
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                 border-radius:6px; padding:16px 20px; margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
                    <span style="font-size:2rem;">🛍️</span>
                    <div style="flex:1;">
                        <div style="font-family:'Playfair Display',serif; font-size:1rem; color:var(--text-primary);">{gname}</div>
                        <div style="font-size:0.8rem; color:var(--text-muted);">{designer or '—'} · {era or '—'}</div>
                        <div style="font-size:0.9rem; color:var(--accent-gold); margin-top:4px;">${float(price):,.0f}</div>
                    </div>
                    <div>
                        <span class="badge badge-excellent">✓ {status.capitalize()}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            