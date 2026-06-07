import streamlit as st
import hashlib
from utils.database import get_connection
from utils.components import page_header, section_divider, condition_badge
import mysql.connector

def render():
    page_header("Admin Panel", "Curatorial & System Management")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        _render_login()
        return

    _render_panel()

def _render_login():
    st.markdown("""
    <div style="text-align:center; margin-bottom:32px;">
        <div style="font-size:3rem;">🔐</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.6rem; color:var(--text-primary); margin-top:8px;">Admin Access</div>
        <div style="font-size:0.8rem; color:var(--text-muted); letter-spacing:2px; margin-top:4px;">RESTRICTED · CURATORS ONLY</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        email    = st.text_input("Email", placeholder="admin@retrothreads.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Access Admin Panel", use_container_width=True):
            if email and password:
                conn   = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT user_id, name, role, password_hash
                    FROM users
                    WHERE email = %s AND role = 'admin'
                """, (email,))
                user_row = cursor.fetchone()

                if not user_row:
                    st.error("No admin account found with that email.")
                else:
                    user_id, name, role, stored_hash = user_row
                    entered_md5    = hashlib.md5(password.encode()).hexdigest()
                    entered_sha256 = hashlib.sha256(password.encode()).hexdigest()

                    if password == stored_hash or entered_md5 == stored_hash or entered_sha256 == stored_hash:
                        st.session_state.admin_logged_in = True
                        st.session_state.admin_name      = name
                        st.session_state.admin_email     = email
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
            else:
                st.error("Please enter your email and password.")

        st.markdown("""
        <div style="text-align:center; font-size:0.75rem; color:var(--text-muted); margin-top:12px;">
            Use an email from the <code>users</code> table with role = 'admin'
        </div>
        """, unsafe_allow_html=True)


def _render_panel():
    conn   = get_connection()
    cursor = conn.cursor()

    col_h, col_btn = st.columns([4, 1])
    with col_h:
        admin_name = st.session_state.get("admin_name", "Admin")
        st.markdown(f'<div style="color:var(--text-muted); font-size:0.85rem;">Signed in as: <span style="color:var(--accent-gold);">{admin_name}</span></div>', unsafe_allow_html=True)
    with col_btn:
        if st.button("Sign Out"):
            st.session_state.admin_logged_in = False
            st.rerun()

    # ── Stats ──────────────────────────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM approval WHERE approval_status = 'Pending'")
    pending_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM garment")
    garment_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM listing")
    listing_count = cursor.fetchone()[0]

    c1, c2, c3, c4 = st.columns(4)
    for col, (num, label) in zip(
        [c1, c2, c3, c4],
        [(pending_count, "Pending Reviews"), (garment_count, "Total Garments"),
         (user_count, "Total Users"), (listing_count, "Total Listings")]
    ):
        with col:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Added two new tabs for User and Listing Management
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Pending Submissions", "✅ Approved Garments", "👤 Designer Registry", "👥 User Management", "🛒 Listing Management"])

    # ── Tab 1: Pending ─────────────────────────────────────────────────────────
    with tab1:
        section_divider("Awaiting Approval")
        st.markdown('<p style="font-size:0.8rem; color:var(--text-muted);">These entries were automatically queued by the <code>initialize_garment_approval</code> trigger when garments were inserted.</p>', unsafe_allow_html=True)

        cursor.execute("""
            SELECT
                a.approval_id,
                a.entity_id,
                a.approval_status,
                g.name                   AS garment_name,
                d.name                   AS designer_name,
                CONCAT(e.start_year,'s') AS era,
                a.approval_date
            FROM approval a
            JOIN      garment  g ON a.entity_id   = g.garment_id
            LEFT JOIN designer d ON g.designer_id  = d.designer_id
            LEFT JOIN era      e ON g.era_id       = e.era_id
            WHERE a.entity_type     = 'GARMENT'
            AND   a.approval_status = 'Pending'
        """)
        pending_rows = cursor.fetchall()

        if not pending_rows:
            st.info("No pending approvals.")
        else:
            for approval_id, entity_id, status, gname, designer, era, approval_date in pending_rows:
                cursor.execute("""
                    SELECT u.name, u.email
                    FROM listing l
                    JOIN users u ON l.seller_id = u.user_id
                    WHERE l.garment_id = %s
                    LIMIT 1
                """, (entity_id,))
                seller_row   = cursor.fetchone()
                seller_name  = seller_row[0] if seller_row else "—"
                seller_email = seller_row[1] if seller_row else "—"

                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                     border-radius:6px; padding:16px 20px; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <span style="font-size:1.8rem;">👗</span>
                        <div style="flex:1;">
                            <div style="font-family:'Playfair Display',serif; font-size:1rem; color:var(--text-primary);">{gname}</div>
                            <div style="font-size:0.8rem; color:var(--text-muted);">{designer or '—'} · {era or '—'}</div>
                            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">
                                Submitted by: {seller_name} ({seller_email}) · {approval_date}
                            </div>
                        </div>
                        <span class="badge badge-good">Pending</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                a_col, r_col, _ = st.columns([1, 1, 4])
                with a_col:
                    if st.button("✓ Approve", key=f"approve_{approval_id}", use_container_width=True):
                        cursor.execute("UPDATE approval SET approval_status = 'Approved' WHERE approval_id = %s", (approval_id,))
                        conn.commit()
                        st.success("Approved!")
                        st.rerun()
                with r_col:
                    if st.button("✗ Reject", key=f"reject_{approval_id}", use_container_width=True):
                        cursor.execute("UPDATE approval SET approval_status = 'Rejected' WHERE approval_id = %s", (approval_id,))
                        conn.commit()
                        st.warning("Rejected.")
                        st.rerun()

    # ── Tab 2: Approved Garments ───────────────────────────────────────────────
    with tab2:
        section_divider("Approved Collection")
        cursor.execute("""
            SELECT g.garment_id, g.name, d.name AS designer,
                   CONCAT(e.start_year,'s') AS era,
                   g.material, g.`condition`
            FROM garment g
            LEFT JOIN designer d ON g.designer_id  = d.designer_id
            LEFT JOIN era      e ON g.era_id        = e.era_id
            JOIN approval a      ON a.entity_id     = g.garment_id
                                AND a.entity_type   = 'GARMENT'
                                AND a.approval_status = 'Approved'
        """)
        approved = cursor.fetchall()

        if not approved:
            st.info("No approved garments yet.")
        else:
            for gid, gname, designer, era, material, cond in approved:
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                     border-radius:6px; padding:14px 20px; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <span style="font-size:1.5rem;">👗</span>
                        <div style="flex:1;">
                            <div style="font-family:'Playfair Display',serif; font-size:0.95rem; color:var(--text-primary);">{gname}</div>
                            <div style="font-size:0.75rem; color:var(--text-muted);">{designer or '—'} · {era or '—'} · {material or '—'}</div>
                        </div>
                        <div>{condition_badge(cond)}</div>
                        <span class="badge badge-excellent">Approved</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 3: Designer Registry ───────────────────────────────────────────────
    with tab3:
        section_divider("Designer Verification")
        cursor.execute("""
            SELECT d.designer_id, d.name, d.nationality, d.birth_year,
                   COUNT(g.garment_id) AS garment_count
            FROM designer d
            LEFT JOIN garment g ON g.designer_id = d.designer_id
            GROUP BY d.designer_id, d.name, d.nationality, d.birth_year
            ORDER BY d.name
        """)
        designers = cursor.fetchall()

        if not designers:
            st.info("No designers found.")
        else:
            for did, dname, nationality, birth_year, count in designers:
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                     border-radius:6px; padding:14px 20px; margin-bottom:8px;
                     display:flex; align-items:center; justify-content:space-between;">
                    <div>
                        <div style="font-family:'Playfair Display',serif; font-size:0.95rem; color:var(--text-primary);">{dname}</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">{nationality or '—'} · b. {birth_year or '—'} · {count} garment{'s' if count != 1 else ''}</div>
                    </div>
                    <span class="badge badge-excellent">✓ Verified</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section_divider("Add New Designer")
        with st.form("add_designer"):
            d1, d2 = st.columns(2)
            with d1:
                new_name    = st.text_input("Designer Name")
                nationality = st.text_input("Nationality")
            with d2:
                birth_year = st.text_input("Birth Year")
                biography  = st.text_area("Biography", height=80)
            if st.form_submit_button("Add & Verify Designer", use_container_width=True):
                if new_name:
                    try:
                        cursor.execute("""
                            INSERT INTO designer (name, nationality, birth_year, biography)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            new_name,
                            nationality or None,
                            int(birth_year) if birth_year.strip().isdigit() else None,
                            biography or None
                        ))
                        conn.commit()
                        st.success(f"✓ Designer '{new_name}' added and verified.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Failed to add designer: {ex}")
                else:
                    st.error("Designer name is required.")

    # ── Tab 4: User Management (NEW) ───────────────────────────────────────────
    with tab4:
        section_divider("Database Users")
        
        # Display existing users
        cursor.execute("SELECT user_id, name, email, role, phone_number, registration_date FROM users ORDER BY user_id DESC")
        users = cursor.fetchall()
        
        for uid, uname, uemail, urole, uphone, udate in users:
            role_colors = {"admin": "badge-poor", "seller": "badge-excellent", "buyer": "badge-good"}
            role_badge = role_colors.get(urole, "badge-fair")
            
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                 border-radius:6px; padding:14px 20px; margin-bottom:8px;
                 display:flex; align-items:center; justify-content:space-between;">
                <div style="flex:1;">
                    <div style="font-family:'Playfair Display',serif; font-size:1rem; color:var(--text-primary);">{uname} <span class="badge {role_badge}" style="margin-left:8px;">{urole.upper()}</span></div>
                    <div style="font-size:0.8rem; color:var(--text-muted);">{uemail} · Ph: {uphone or 'N/A'} · Joined: {udate}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Delete user button
            if st.button("🗑️ Delete User", key=f"del_user_{uid}"):
                try:
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (uid,))
                    conn.commit()
                    st.success(f"User {uname} deleted permanently.")
                    st.rerun()
                except mysql.connector.Error as err:
                    st.error(f"Cannot delete user: They likely have associated transactions or listings. Database error: {err}")

        st.markdown("<br>", unsafe_allow_html=True)
        section_divider("Add New User")
        with st.form("add_user_form"):
            u1, u2 = st.columns(2)
            with u1:
                new_uname = st.text_input("Full Name *")
                new_uemail = st.text_input("Email Address *")
                new_urole = st.selectbox("Role *", ["buyer", "seller", "admin"])
            with u2:
                new_upass = st.text_input("Password *", type="password")
                new_uphone = st.text_input("Phone Number")
            
            if st.form_submit_button("Create User in Database", use_container_width=True):
                if new_uname and new_uemail and new_upass:
                    try:
                        cursor.execute("""
                            INSERT INTO users (name, email, role, password_hash, phone_number, registration_date)
                            VALUES (%s, %s, %s, %s, %s, CURDATE())
                        """, (new_uname, new_uemail, new_urole, new_upass, new_uphone or None))
                        conn.commit()
                        st.success(f"User {new_uname} created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating user: {e}")
                else:
                    st.error("Please fill out all required fields (*).")

    # ── Tab 5: Listing Management (NEW) ────────────────────────────────────────
    with tab5:
        section_divider("All Marketplace Listings")
        
        cursor.execute("""
            SELECT l.listing_id, g.name, u.name, l.price, l.status, l.listing_date
            FROM listing l
            JOIN garment g ON l.garment_id = g.garment_id
            JOIN users u ON l.seller_id = u.user_id
            ORDER BY l.listing_id DESC
        """)
        all_listings = cursor.fetchall()
        
        if not all_listings:
            st.info("No listings in the database.")
        else:
            for lid, lgname, seller, lprice, lstatus, ldate in all_listings:
                stat_badge = "badge-poor" if lstatus == 'sold' else "badge-excellent"
                
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle);
                     border-radius:6px; padding:14px 20px; margin-bottom:8px;
                     display:flex; align-items:center; justify-content:space-between;">
                    <div style="flex:1;">
                        <div style="font-family:'Playfair Display',serif; font-size:1rem; color:var(--text-primary);">[ID: {lid}] {lgname}</div>
                        <div style="font-size:0.8rem; color:var(--text-muted);">Seller: {seller} · Listed: {ldate} · <span style="color:var(--accent-gold);">${lprice:,.0f}</span></div>
                    </div>
                    <span class="badge {stat_badge}">{lstatus.upper()}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗑️ Force Delete Listing", key=f"del_listing_{lid}"):
                    try:
                        cursor.execute("DELETE FROM listing WHERE listing_id = %s", (lid,))
                        conn.commit()
                        st.success("Listing removed from database.")
                        st.rerun()
                    except mysql.connector.Error as err:
                        st.error(f"Cannot delete listing. It may be tied to a completed transaction. Database error: {err}")