import streamlit as st

def page_header(title: str, subtitle: str = ""):
    subtitle_html = f'<div class="page-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
<div class="page-header">
<div class="page-title">{title}</div>
{subtitle_html}
<div class="gold-line"></div>
</div>
""", unsafe_allow_html=True)


def condition_badge(condition: str) -> str:
    mapping = {
        "Excellent": "badge-excellent",
        "Good": "badge-good",
        "Fair": "badge-fair",
        "Poor": "badge-poor",
    }
    cls = mapping.get(condition, "badge-good")
    return f'<span class="badge {cls}">{condition}</span>'


def style_tags_html(tags: list) -> str:
    html = ""
    for tag in tags:
        html += f'<span class="tag tag-gold">{tag}</span>'
    return html


def garment_card_html(garment: dict, show_price: bool = False, price: float = None):
    cond_badge = condition_badge(garment.get("condition", ""))
    
    # Safely handle tags if they are missing
    raw_tags = garment.get("style_tags", [])
    tags = style_tags_html(raw_tags[:3]) if raw_tags else ""
    
    price_html = f'<div class="garment-card-price">${price:,.0f}</div>' if show_price and price else ""
    
    # ALL indentation removed to prevent Streamlit Markdown code-block rendering
    return f"""
<div class="garment-card">
<div style="height:200px; display:flex; align-items:center; justify-content:center; font-size:5rem; background:linear-gradient(135deg,#1a1714,#211e1a);">
{garment.get('icon', '👗')}
</div>
<div class="garment-card-body">
<div class="garment-card-name">{garment.get('name', '')}</div>
<div class="garment-card-meta">{garment.get('designer', '')} &middot; {garment.get('era', '')}</div>
<div style="margin-top:6px;">{cond_badge}</div>
<div style="margin-top:8px;">{tags}</div>
{price_html}
</div>
</div>
"""


def stat_card(number, label):
    st.markdown(f"""
<div class="stat-card">
<div class="stat-number">{number}</div>
<div class="stat-label">{label}</div>
</div>
""", unsafe_allow_html=True)


def section_divider(title: str = ""):
    if title:
        st.markdown(f'<div class="detail-section-title">{title}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<hr>', unsafe_allow_html=True)


def timeline_event(date: str, title: str, description: str, event_type: str = ""):
    type_colors = {
        "Runway Show": "#c9a84c",
        "Celebrity": "#b87333",
        "Museum Exhibition": "#5a8a6a",
        "Media": "#6a7a8a",
        "Sale": "#8a6a5a",
    }
    color = type_colors.get(event_type, "#a89880")
    tag_html = f'<span class="tag" style="border-color:{color}; color:{color};">{event_type}</span>' if event_type else ''
    
    st.markdown(f"""
<div class="timeline-item">
<div class="timeline-date">{date}</div>
<div class="timeline-title">{title}</div>
{tag_html}
<div class="timeline-desc">{description}</div>
</div>
""", unsafe_allow_html=True)
    

    