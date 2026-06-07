import streamlit as st

def inject_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

    :root {
        --bg-primary: #0d0b08;
        --bg-secondary: #141210;
        --bg-card: #1a1714;
        --bg-card-hover: #211e1a;
        --accent-gold: #c9a84c;
        --accent-gold-light: #e8c97a;
        --accent-copper: #b87333;
        --text-primary: #f0e8d8;
        --text-secondary: #a89880;
        --text-muted: #6b5e4e;
        --border-subtle: #2a2420;
        --border-accent: #3d3228;
        --success: #5a8a6a;
        --warning: #b87333;
        --danger: #8a4a4a;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Cormorant Garamond', serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-accent) !important;
    }

    [data-testid="stSidebar"] * {
        font-family: 'Cormorant Garamond', serif !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: none !important;
        text-align: left !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px;
        padding: 10px 16px !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: var(--bg-card) !important;
        color: var(--accent-gold) !important;
    }

    .page-header {
        padding: 32px 0 24px;
        border-bottom: 1px solid var(--border-accent);
        margin-bottom: 32px;
    }
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        color: var(--text-primary);
        letter-spacing: 1px;
        margin: 0;
        line-height: 1.1;
    }
    .page-subtitle {
        font-size: 1rem;
        color: var(--text-muted);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 6px;
    }
    .gold-line {
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-gold), transparent);
        margin: 12px 0;
    }

    .garment-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 6px;
        padding: 0;
        overflow: hidden;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    .garment-card:hover {
        border-color: var(--accent-gold);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(201,168,76,0.08);
    }
    .garment-card-body { padding: 16px; }
    .garment-card-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        color: var(--text-primary);
        margin: 0 0 4px;
    }
    .garment-card-meta {
        font-size: 0.8rem;
        color: var(--text-muted);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 2px 0;
    }
    .garment-card-price {
        font-family: 'DM Mono', monospace;
        font-size: 1rem;
        color: var(--accent-gold);
        margin-top: 8px;
    }

    .tag {
        display: inline-block;
        background: var(--bg-secondary);
        border: 1px solid var(--border-accent);
        color: var(--text-secondary);
        font-size: 0.65rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 2px;
        margin: 2px 2px 2px 0;
    }
    .tag-gold {
        border-color: var(--accent-gold);
        color: var(--accent-gold);
    }

    .badge {
        display: inline-block;
        font-size: 0.65rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 2px;
        font-weight: 500;
    }
    .badge-excellent { background: #1a2e22; color: #5a8a6a; border: 1px solid #2a4a32; }
    .badge-good { background: #2a2010; color: #c9a84c; border: 1px solid #3a3018; }
    .badge-fair { background: #2a1a10; color: #b87333; border: 1px solid #3a2a18; }
    .badge-poor { background: #2a1010; color: #8a4a4a; border: 1px solid #3a1818; }

    .timeline-item {
        border-left: 2px solid var(--border-accent);
        padding: 0 0 32px 24px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        width: 10px;
        height: 10px;
        background: var(--accent-gold);
        border-radius: 50%;
        position: absolute;
        left: -6px;
        top: 4px;
    }
    .timeline-date {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: var(--accent-gold);
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .timeline-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        color: var(--text-primary);
    }
    .timeline-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 6px;
        line-height: 1.6;
    }

    .filter-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 24px;
    }
    .filter-title {
        font-family: 'Playfair Display', serif;
        font-size: 0.8rem;
        color: var(--text-muted);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-accent) !important;
        color: var(--text-primary) !important;
        border-radius: 4px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 1px var(--accent-gold) !important;
    }
    label { color: var(--text-secondary) !important; font-family: 'Cormorant Garamond', serif !important; }

    .stButton > button {
        background: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-accent) !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        border-color: var(--accent-gold) !important;
        color: var(--accent-gold) !important;
        background: rgba(201,168,76,0.08) !important;
    }

    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 6px;
        padding: 20px 24px;
        text-align: center;
    }
    .stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: var(--accent-gold);
        line-height: 1;
    }
    .stat-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    .hero-section {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
        border: 1px solid var(--border-accent);
        border-radius: 8px;
        padding: 60px 48px;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '🧵';
        position: absolute;
        right: 48px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 8rem;
        opacity: 0.06;
    }
    .hero-eyebrow {
        font-size: 0.7rem;
        color: var(--accent-gold);
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        color: var(--text-primary);
        line-height: 1.1;
        margin: 0 0 16px;
    }
    .hero-title em {
        color: var(--accent-gold);
        font-style: italic;
    }
    .hero-body {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 520px;
        line-height: 1.7;
        margin-bottom: 28px;
    }

    .detail-section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        color: var(--text-muted);
        letter-spacing: 3px;
        text-transform: uppercase;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 8px;
        margin: 24px 0 16px;
    }
    .detail-value {
        font-size: 1rem;
        color: var(--text-primary);
    }
    .detail-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    hr { border-color: var(--border-subtle) !important; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--text-primary) !important; }
    p { color: var(--text-secondary) !important; }
    </style>
    """, unsafe_allow_html=True)