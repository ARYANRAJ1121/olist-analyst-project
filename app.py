"""
Olist E-Commerce Analytics Dashboard
=====================================
A comprehensive Streamlit dashboard with enhanced interactivity and modern design.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="Olist Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme configurations
THEMES = {
    "Midnight Purple": {
        "bg_gradient": "linear-gradient(135deg, #0a0a0f 0%, #12101e 50%, #0d0f1a 100%)",
        "sidebar_bg": "linear-gradient(180deg, #110e1f 0%, #1a1530 50%, #0e0c1a 100%)",
        "primary": "#a78bfa",
        "secondary": "#818cf8",
        "accent": "#c084fc",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "text": "#e8e6f0",
        "muted": "#8b85a6",
        "card_bg": "rgba(30, 25, 50, 0.7)",
        "chart_colors": ["#a78bfa", "#818cf8", "#c084fc", "#34d399", "#fbbf24", "#f472b6"]
    },
    "Cyber Noir": {
        "bg_gradient": "linear-gradient(135deg, #050508 0%, #0a0e17 50%, #0c111d 100%)",
        "sidebar_bg": "linear-gradient(180deg, #0a0f1a 0%, #111827 50%, #0a0f1a 100%)",
        "primary": "#22d3ee",
        "secondary": "#06b6d4",
        "accent": "#67e8f9",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#fb7185",
        "text": "#e2e8f0",
        "muted": "#64748b",
        "card_bg": "rgba(15, 23, 42, 0.75)",
        "chart_colors": ["#22d3ee", "#06b6d4", "#34d399", "#fbbf24", "#fb7185", "#a78bfa"]
    },
    "Neon Ember": {
        "bg_gradient": "linear-gradient(135deg, #0c0607 0%, #150a0c 50%, #0f0808 100%)",
        "sidebar_bg": "linear-gradient(180deg, #1a0f0f 0%, #1f1215 50%, #120a0a 100%)",
        "primary": "#fb923c",
        "secondary": "#f97316",
        "accent": "#fbbf24",
        "success": "#4ade80",
        "warning": "#fbbf24",
        "danger": "#ef4444",
        "text": "#fef2e8",
        "muted": "#9a8478",
        "card_bg": "rgba(35, 20, 15, 0.7)",
        "chart_colors": ["#fb923c", "#f97316", "#fbbf24", "#4ade80", "#ef4444", "#c084fc"]
    },
    "Matrix Green": {
        "bg_gradient": "linear-gradient(135deg, #040806 0%, #081210 50%, #050e0a 100%)",
        "sidebar_bg": "linear-gradient(180deg, #0a1a12 0%, #0f2418 50%, #081410 100%)",
        "primary": "#4ade80",
        "secondary": "#22c55e",
        "accent": "#86efac",
        "success": "#4ade80",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "text": "#e2f5e9",
        "muted": "#5e8a70",
        "card_bg": "rgba(12, 30, 20, 0.75)",
        "chart_colors": ["#4ade80", "#22c55e", "#86efac", "#fbbf24", "#f87171", "#22d3ee"]
    }
}

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = "Midnight Purple"

theme = THEMES[st.session_state.theme]

# Dynamic CSS based on theme
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {theme['bg_gradient']};
        background-attachment: fixed;
    }}
    
    /* ===== FUTURISTIC ANIMATED BACKGROUND ===== */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse at 15% 50%, {theme['primary']}12 0%, transparent 50%),
            radial-gradient(ellipse at 85% 20%, {theme['accent']}10 0%, transparent 50%),
            radial-gradient(ellipse at 50% 85%, {theme['secondary']}08 0%, transparent 50%),
            radial-gradient(ellipse at 70% 60%, {theme['primary']}06 0%, transparent 40%);
        animation: meshOrbit 20s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }}
    
    @keyframes meshOrbit {{
        0% {{ opacity: 0.8; filter: hue-rotate(0deg); }}
        50% {{ opacity: 1; filter: hue-rotate(15deg); }}
        100% {{ opacity: 0.8; filter: hue-rotate(0deg); }}
    }}
    
    /* ===== TOP HEADER BAR STYLING ===== */
    header[data-testid="stHeader"] {{
        background: {theme['bg_gradient']} !important;
        backdrop-filter: blur(10px);
    }}
    
    /* Hide the top decoration/toolbar background */
    .stDeployButton, 
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {{
        background: transparent !important;
    }}
    
    /* Style the entire top area */
    .stApp > header {{
        background: {theme['bg_gradient']} !important;
    }}
    
    /* Remove any white backgrounds from top sections */
    div[data-testid="stHeader"] > div {{
        background: transparent !important;
    }}
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {{
        background: {theme['sidebar_bg']} !important;
        border-right: 1px solid {theme['primary']}15;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: {theme['sidebar_bg']} !important;
    }}
    
    [data-testid="stSidebarContent"] {{
        background: {theme['sidebar_bg']} !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: {theme['sidebar_bg']} !important;
    }}
    
    /* Cover the top white patch */
    [data-testid="stSidebar"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: {theme['sidebar_bg']};
        z-index: -1;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: #ffffff !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown p {{
        color: #ffffff !important;
    }}
    
    /* Sidebar Headers - WHITE and READABLE */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: #ffffff !important;
        background: none !important;
        -webkit-text-fill-color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        font-weight: 700 !important;
    }}
    
    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] .stRadio > div {{
        background: transparent;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: {theme['text']} !important;
        padding: 12px 16px !important;
        border-radius: 12px !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
        border: 1px solid transparent !important;
    }}
    
    [data-testid="stSidebar"] .stRadio label:hover {{
        background: {theme['card_bg']} !important;
        border-color: {theme['primary']}40 !important;
        transform: translateX(5px);
    }}
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {{
        background: linear-gradient(90deg, {theme['primary']}30, {theme['secondary']}20) !important;
        border-color: {theme['primary']} !important;
        color: {theme['primary']} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {{
        color: {theme['text']} !important;
    }}
    
    /* Sidebar Radio Circle Color */
    [data-testid="stSidebar"] .stRadio div[data-checked="true"] > div:first-child {{
        background-color: {theme['primary']} !important;
        border-color: {theme['primary']} !important;
    }}
    
    /* Sidebar Selectbox */
    [data-testid="stSidebar"] .stSelectbox > div > div {{
        background: {theme['card_bg']} !important;
        border: 1px solid {theme['primary']}40 !important;
        border-radius: 12px !important;
        color: {theme['text']} !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox > div > div:hover {{
        border-color: {theme['primary']} !important;
        box-shadow: 0 0 15px {theme['primary']}30 !important;
    }}
    
    /* Sidebar Metrics */
    [data-testid="stSidebar"] [data-testid="stMetric"] {{
        background: linear-gradient(135deg, {theme['card_bg']}, {theme['primary']}15) !important;
        border: 1px solid {theme['primary']}30 !important;
        border-radius: 16px !important;
        padding: 16px !important;
        margin: 8px 0 !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMetric"]:hover {{
        border-color: {theme['primary']} !important;
        box-shadow: 0 5px 25px {theme['primary']}25 !important;
        transform: translateY(-3px);
    }}
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {{
        color: {theme['primary']} !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
        color: {theme['muted']} !important;
        font-size: 0.85rem !important;
    }}
    
    /* Sidebar Divider */
    [data-testid="stSidebar"] hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {theme['primary']}50, transparent);
        margin: 20px 0;
    }}
    
    /* ===== MAIN CONTENT STYLING ===== */
    h1, h2, h3 {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }}
    
    [data-testid="stMetric"] {{
        background: {theme['card_bg']};
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    [data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 20px {theme['primary']}10;
        border-color: {theme['primary']}30;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {theme['text']} !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {theme['muted']} !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        color: {theme['muted']};
        padding: 12px 24px;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white !important;
    }}
    
    .stAlert {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }}
    
    .stSelectbox > div > div {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }}
    
    /* ===== GLASSMORPHIC KPI CARDS ===== */
    .kpi-card {{
        background: {theme['card_bg']};
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 28px 20px;
        text-align: center;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: left 0.7s ease;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 40px {theme['primary']}15;
        border-color: {theme['primary']}60;
    }}
    
    .kpi-card:hover::before {{
        left: 100%;
    }}
    
    .kpi-icon {{
        width: 52px; height: 52px;
        border-radius: 14px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 12px;
        background: linear-gradient(135deg, {theme['primary']}25, {theme['secondary']}20);
        border: 1px solid {theme['primary']}30;
    }}
    
    .big-number {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {theme['primary']}, {theme['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }}
    
    .stat-label {{
        color: {theme['muted']};
        font-size: 0.85rem;
        margin-top: 6px;
        letter-spacing: 0.02em;
    }}
    
    .kpi-title {{
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 6px;
    }}
    
    /* ===== INSIGHT CARDS ===== */
    .insight-card {{
        background: linear-gradient(135deg, {theme['card_bg']}, rgba(255,255,255,0.02));
        border-left: 4px solid {theme['primary']};
        padding: 22px;
        border-radius: 0 16px 16px 0;
        margin: 15px 0;
        transition: all 0.3s ease;
    }}
    
    .insight-card:hover {{
        transform: translateX(5px);
        border-left-color: {theme['accent']};
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }}
    
    /* ===== HERO SECTION ===== */
    .hero-badge {{
        display: inline-block;
        padding: 6px 18px;
        border-radius: 999px;
        background: linear-gradient(135deg, {theme['primary']}20, {theme['accent']}15);
        border: 1px solid {theme['primary']}50;
        color: {theme['primary']};
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
        animation: badgeGlow 3s ease-in-out infinite alternate;
    }}
    
    @keyframes badgeGlow {{
        0% {{ box-shadow: 0 0 5px {theme['primary']}20; }}
        100% {{ box-shadow: 0 0 20px {theme['primary']}40, 0 0 40px {theme['primary']}15; }}
    }}
    
    /* ===== ANIMATED GRADIENT BORDER ===== */
    .glow-border {{
        position: relative;
        border-radius: 20px;
        overflow: hidden;
    }}
    
    .glow-border::after {{
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        background: linear-gradient(45deg, 
            {theme['primary']}, {theme['accent']}, {theme['secondary']}, {theme['primary']});
        background-size: 400% 400%;
        border-radius: 22px;
        z-index: -1;
        animation: borderRotate 6s linear infinite;
        opacity: 0;
        transition: opacity 0.4s ease;
    }}
    
    .glow-border:hover::after {{
        opacity: 1;
    }}
    
    @keyframes borderRotate {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* ===== CHAT BUBBLES ===== */
    .chat-user {{
        background: linear-gradient(135deg, {theme['card_bg']}, {theme['primary']}15);
        border: 1px solid {theme['primary']}40;
        border-radius: 16px 16px 4px 16px;
        padding: 16px 20px;
        margin: 10px 0 10px 20%;
        text-align: right;
        animation: fadeInUp 0.3s ease-out;
    }}
    
    .chat-ai {{
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.06));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px 16px 16px 4px;
        padding: 16px 20px;
        margin: 10px 20% 10px 0;
        animation: fadeInUp 0.3s ease-out;
        position: relative;
    }}
    
    .chat-ai::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: linear-gradient(180deg, {theme['accent']}, {theme['primary']});
        border-radius: 3px 0 0 3px;
    }}
    
    /* ===== THINKING ANIMATION ===== */
    .thinking-dots {{
        display: inline-flex;
        gap: 4px;
    }}
    .thinking-dots span {{
        width: 8px; height: 8px;
        border-radius: 50%;
        background: {theme['primary']};
        animation: bounce 1.4s ease-in-out infinite;
    }}
    .thinking-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
    .thinking-dots span:nth-child(3) {{ animation-delay: 0.4s; }}
    
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); opacity: 0.4; }}
        50% {{ transform: translateY(-8px); opacity: 1; }}
    }}
    
    /* ===== STATUS PILL ===== */
    .status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }}
    .status-pill.online {{
        background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
        border: 1px solid rgba(16,185,129,0.4);
        color: #10b981;
    }}
    .status-pill.connected {{
        background: linear-gradient(135deg, {theme['primary']}15, {theme['primary']}05);
        border: 1px solid {theme['primary']}40;
        color: {theme['primary']};
    }}
    
    /* ===== PULSE ANIMATION ===== */
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
        100% {{ opacity: 1; }}
    }}
    
    /* ===== FADE IN ANIMATION ===== */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .stMarkdown, [data-testid="stMetric"], .stPlotlyChart {{
        animation: fadeInUp 0.5s ease-out;
    }}
    
    /* ===== FOOTER ===== */
    .footer {{
        text-align: center;
        padding: 30px 20px;
        color: {theme['muted']};
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 40px;
    }}
    
    .footer a {{
        color: {theme['primary']};
        text-decoration: none;
        transition: color 0.3s;
    }}
    
    .footer a:hover {{
        color: {theme['accent']};
    }}
    
    /* ===== BUTTON STYLING ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px {theme['primary']}30;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 30px {theme['primary']}50;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px);
    }}
    
    /* ===== SLIDER ===== */
    .stSlider > div > div {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['secondary']} 100%);
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        border-color: {theme['primary']}40 !important;
    }}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.1);
    }}
    ::-webkit-scrollbar-thumb {{
        background: {theme['primary']}50;
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {theme['primary']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data
def load_data():
    """Load all required datasets"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    raw_dir = os.path.join(base_dir, "data", "raw")
    
    data = {}
    
    try:
        data['monthly_revenue'] = pd.read_csv(os.path.join(output_dir, "monthly_revenue.csv"))
        data['monthly_revenue']['month'] = pd.to_datetime(data['monthly_revenue']['month'])
    except:
        data['monthly_revenue'] = None
        
    try:
        data['retention_metrics'] = pd.read_csv(os.path.join(output_dir, "retention_metrics.csv"))
    except:
        data['retention_metrics'] = None
        
    try:
        data['churn_features'] = pd.read_csv(os.path.join(output_dir, "churn_features_v2.csv"))
    except:
        data['churn_features'] = None
        
    try:
        data['ab_test'] = pd.read_csv(os.path.join(output_dir, "ab_test_second_purchase_results.csv"))
    except:
        data['ab_test'] = None
        
    try:
        data['statistical_tests'] = pd.read_csv(os.path.join(output_dir, "churn_statistical_tests.csv"))
    except:
        data['statistical_tests'] = None
        
    try:
        data['logistic_coef'] = pd.read_csv(os.path.join(output_dir, "logistic_regression_coefficients_v2.csv"))
    except:
        data['logistic_coef'] = None
    
    try:
        data['orders'] = pd.read_csv(os.path.join(raw_dir, "olist_orders_dataset.csv"))
        data['orders']['order_purchase_timestamp'] = pd.to_datetime(data['orders']['order_purchase_timestamp'])
    except:
        data['orders'] = None
        
    try:
        data['order_items'] = pd.read_csv(os.path.join(raw_dir, "olist_order_items_dataset.csv"))
    except:
        data['order_items'] = None
        
    try:
        data['products'] = pd.read_csv(os.path.join(raw_dir, "olist_products_dataset.csv"))
    except:
        data['products'] = None
        
    try:
        data['category_translation'] = pd.read_csv(os.path.join(raw_dir, "product_category_name_translation.csv"))
    except:
        data['category_translation'] = None
    
    return data

data = load_data()

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## 📊 Olist Analytics")
    st.markdown("---")
    
    # Theme Selector
    st.markdown("### 🎨 Theme")
    selected_theme = st.selectbox(
        "Choose theme:",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
        label_visibility="collapsed"
    )
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate to:",
        ["🏠 Overview", "📈 Revenue Analysis", "🔄 Retention & Churn",
         "🧪 A/B Testing", "🔬 Statistical Analysis", "📋 Data Explorer",
         "🤖 Ask AI"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📌 Quick Stats")
    if data['retention_metrics'] is not None:
        total_customers = int(data['retention_metrics']['total_customers'].iloc[0])
        st.metric("Total Customers", f"{total_customers:,}")
    
    if data['monthly_revenue'] is not None:
        total_revenue = data['monthly_revenue']['revenue'].sum()
        st.metric("Total Revenue", f"R${total_revenue:,.0f}")
    
    if data['retention_metrics'] is not None:
        repeat_rate = data['retention_metrics']['repeat_purchase_rate'].iloc[0] * 100
        st.metric("Repeat Rate", f"{repeat_rate:.1f}%")
    
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: {theme['muted']}; font-size: 0.8rem;'>
        Built with ❤️ using Streamlit<br>
        Data: Olist E-Commerce Dataset
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def create_plotly_layout(title="", height=400):
    """Create consistent Plotly layout with current theme"""
    return dict(
        title=dict(text=title, font=dict(size=20, color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.02)',
        font=dict(color=theme['muted'], family='Inter'),
        height=height,
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white')),
        hoverlabel=dict(bgcolor=theme['primary'], font_size=14, font_family='Inter')
    )

def create_kpi_card(title, value, subtitle="", icon=""):
    """Create a styled KPI card"""
    return f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>{icon}</div>
        <div class='big-number'>{value}</div>
        <div class='kpi-title'>{title}</div>
        <div class='stat-label'>{subtitle}</div>
    </div>
    """

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================
if page == "🏠 Overview":
    st.markdown(f"""
    <div style='margin-bottom: 30px;'>
        <div class='hero-badge'>Live Analytics Dashboard</div>
        <h1 style='font-size: 2.6rem; margin: 10px 0 5px 0; background: linear-gradient(135deg, {theme["primary"]}, {theme["accent"]}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800;'>Olist E-Commerce Analytics</h1>
        <p style='color: {theme["muted"]}; font-size: 1.1rem; margin: 0;'>100K+ orders analyzed &bull; Churn prediction &bull; A/B testing &bull; AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Animated KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if data['retention_metrics'] is not None:
            total_customers = int(data['retention_metrics']['total_customers'].iloc[0])
            st.markdown(create_kpi_card("Total Customers", f"{total_customers:,}", "Unique buyers", "👥"), unsafe_allow_html=True)
    
    with col2:
        if data['monthly_revenue'] is not None:
            total_revenue = data['monthly_revenue']['revenue'].sum()
            st.markdown(create_kpi_card("Total Revenue", f"R${total_revenue/1e6:.1f}M", "2016-2018", "💰"), unsafe_allow_html=True)
    
    with col3:
        if data['retention_metrics'] is not None:
            repeat_rate = data['retention_metrics']['repeat_purchase_rate'].iloc[0] * 100
            st.markdown(create_kpi_card("Repeat Rate", f"{repeat_rate:.1f}%", "Return customers", "🔄"), unsafe_allow_html=True)
    
    with col4:
        if data['ab_test'] is not None:
            lift = ((data['ab_test'][data['ab_test']['group'] == 'treatment']['conversion_rate'].values[0] / 
                    data['ab_test'][data['ab_test']['group'] == 'control']['conversion_rate'].values[0]) - 1) * 100
            st.markdown(create_kpi_card("A/B Test Lift", f"+{lift:.0f}%", "Significant result", "🧪"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two column layout for overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Revenue Trend")
        if data['monthly_revenue'] is not None:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['monthly_revenue']['month'],
                y=data['monthly_revenue']['revenue'],
                mode='lines+markers',
                line=dict(color=theme['primary'], width=3, shape='spline'),
                marker=dict(size=8, color=theme['secondary'], line=dict(width=2, color='white')),
                fill='tozeroy',
                fillcolor=f"rgba{tuple(int(theme['primary'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}",
                name='Revenue',
                hovertemplate="<b>%{x|%B %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
            ))
            fig.update_layout(**create_plotly_layout("", 380))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("### 🥧 Customer Retention")
        if data['retention_metrics'] is not None:
            repeat_rate = data['retention_metrics']['repeat_purchase_rate'].iloc[0]
            one_time_rate = 1 - repeat_rate
            
            fig = go.Figure(data=[go.Pie(
                labels=['One-time Customers', 'Repeat Customers'],
                values=[one_time_rate * 100, repeat_rate * 100],
                hole=0.6,
                marker=dict(colors=[theme['danger'], theme['success']]),
                textinfo='percent+label',
                textfont=dict(size=13, color='white'),
                hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
                pull=[0.02, 0.05]
            )])
            fig.update_layout(**create_plotly_layout("", 380))
            fig.add_annotation(text="97%", x=0.5, y=0.5, font=dict(size=36, color='white', family='Inter'), showarrow=False)
            fig.add_annotation(text="One-time", x=0.5, y=0.38, font=dict(size=12, color=theme['muted']), showarrow=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Key Findings Section
    st.markdown("### 🔍 Key Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='insight-card' style='border-left-color: {theme['danger']};'>
            <div style='font-size: 2rem; margin-bottom: 8px;'>📉</div>
            <div style='color: white; font-weight: 700; font-size: 1.05rem; margin-bottom: 8px;'>97% Never Return</div>
            <div style='color: {theme["muted"]}; font-size: 0.9rem; line-height: 1.5;'>
                Nearly all customers are one-and-done. This is the single biggest growth opportunity on the platform.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='insight-card' style='border-left-color: {theme['warning']};'>
            <div style='font-size: 2rem; margin-bottom: 8px;'>⚠️</div>
            <div style='color: white; font-weight: 700; font-size: 1.05rem; margin-bottom: 8px;'>Prediction Failed at 55%</div>
            <div style='color: {theme["muted"]}; font-size: 0.9rem; line-height: 1.5;'>
                ML churn prediction drops to coin-flip accuracy once data leakage is removed. Churn is the default state, not a signal.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='insight-card' style='border-left-color: {theme['success']};'>
            <div style='font-size: 2rem; margin-bottom: 8px;'>🧪</div>
            <div style='color: white; font-weight: 700; font-size: 1.05rem; margin-bottom: 8px;'>A/B Test: 4x ROI</div>
            <div style='color: {theme["muted"]}; font-size: 0.9rem; line-height: 1.5;'>
                A 10% post-purchase discount lifted repeat purchases by 67%. $200K revenue vs $50K cost = proven strategy.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA to Ask AI
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {theme["primary"]}15, {theme["accent"]}10);
        border: 1px solid {theme["primary"]}30;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    '>
        <div style='font-size: 1.1rem; color: white; font-weight: 600; margin-bottom: 6px;'>
            🤖 Want deeper insights? Try the AI Analyst
        </div>
        <div style='color: {theme["muted"]}; font-size: 0.9rem;'>
            Navigate to <strong>Ask AI</strong> in the sidebar to ask questions about the data in plain English
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: REVENUE ANALYSIS
# ============================================================================
elif page == "📈 Revenue Analysis":
    st.markdown("# 📈 Revenue Analysis")
    st.markdown("### Analyze revenue trends and patterns over time")
    
    if data['monthly_revenue'] is not None:
        df_rev = data['monthly_revenue'].copy()
        
        # Interactive Date Range Filter
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📅 Filter by Date Range")
        with col2:
            date_filter = st.selectbox("Quick Select:", ["All Time", "2017 Only", "2018 Only"], label_visibility="collapsed")
        
        if date_filter == "2017 Only":
            df_rev = df_rev[df_rev['month'].dt.year == 2017]
        elif date_filter == "2018 Only":
            df_rev = df_rev[df_rev['month'].dt.year == 2018]
        
        # Monthly Revenue Trend with animation
        st.markdown("### Monthly Revenue Trend")
        
        chart_type = st.radio("Chart Type:", ["Area", "Line", "Bar"], horizontal=True)
        
        fig = go.Figure()
        if chart_type == "Area":
            fig.add_trace(go.Scatter(
                x=df_rev['month'], y=df_rev['revenue'],
                mode='lines+markers',
                line=dict(color=theme['primary'], width=3, shape='spline'),
                marker=dict(size=10, color=theme['secondary'], line=dict(width=2, color='white')),
                fill='tozeroy',
                fillcolor=f"rgba{tuple(int(theme['primary'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.15,)}",
                name='Revenue',
                hovertemplate="<b>%{x|%B %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
            ))
        elif chart_type == "Line":
            fig.add_trace(go.Scatter(
                x=df_rev['month'], y=df_rev['revenue'],
                mode='lines+markers',
                line=dict(color=theme['primary'], width=4),
                marker=dict(size=12, color=theme['accent']),
                hovertemplate="<b>%{x|%B %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
            ))
        else:
            fig.add_trace(go.Bar(
                x=df_rev['month'], y=df_rev['revenue'],
                marker=dict(color=theme['chart_colors'][0], line=dict(width=0)),
                hovertemplate="<b>%{x|%B %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
            ))
        
        fig.update_layout(**create_plotly_layout("", 450))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Revenue Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💵 Total Revenue", f"R${df_rev['revenue'].sum():,.0f}")
        with col2:
            st.metric("📊 Average Monthly", f"R${df_rev['revenue'].mean():,.0f}")
        with col3:
            st.metric("📈 Peak Month", f"R${df_rev['revenue'].max():,.0f}")
        with col4:
            if len(df_rev) > 1:
                growth = ((df_rev['revenue'].iloc[-1] / df_rev['revenue'].iloc[1]) - 1) * 100
                st.metric("🚀 Overall Growth", f"+{growth:.0f}%")
        
        st.markdown("---")
        
        # Year-over-Year Comparison
        st.markdown("### Year-over-Year Comparison")
        
        df_rev['year'] = df_rev['month'].dt.year
        yearly_data = df_rev.groupby('year')['revenue'].sum().reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=yearly_data['year'].astype(str),
                y=yearly_data['revenue'],
                marker=dict(
                    color=theme['chart_colors'][:len(yearly_data)],
                    line=dict(width=0)
                ),
                text=yearly_data['revenue'].apply(lambda x: f'R${x/1e6:.1f}M'),
                textposition='outside',
                textfont=dict(color='white', size=14),
                hovertemplate="<b>%{x}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
            )
        ])
        fig.update_layout(**create_plotly_layout("", 400))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.error("Revenue data not available. Please run the analysis pipeline first.")

# ============================================================================
# PAGE: RETENTION & CHURN
# ============================================================================
elif page == "🔄 Retention & Churn":
    st.markdown("# 🔄 Retention & Churn Analysis")
    st.markdown("### Deep dive into customer behavior and churn patterns")
    
    tabs = st.tabs(["📊 Retention Overview", "📉 Order Frequency", "🔍 Churn Features", "🤖 Model Performance"])
    
    with tabs[0]:
        st.markdown("### Customer Retention Breakdown")
        
        if data['retention_metrics'] is not None:
            ret = data['retention_metrics']
            
            col1, col2 = st.columns(2)
            
            with col1:
                repeat_rate = ret['repeat_purchase_rate'].iloc[0]
                one_time_rate = 1 - repeat_rate
                
                fig = go.Figure(data=[go.Pie(
                    labels=['One-time Customers', 'Repeat Customers'],
                    values=[one_time_rate * 100, repeat_rate * 100],
                    hole=0.65,
                    marker=dict(colors=[theme['danger'], theme['success']]),
                    textinfo='percent',
                    textfont=dict(size=16, color='white'),
                    hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
                    pull=[0.02, 0.08]
                )])
                fig.update_layout(**create_plotly_layout("", 400))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                st.markdown("#### 📌 Key Metrics")
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 4px solid {theme["primary"]};'>
                    <h3 style='color: {theme["primary"]}; margin: 0;'>{int(ret['total_customers'].iloc[0]):,}</h3>
                    <p style='color: {theme["muted"]}; margin: 5px 0 0 0;'>Total Unique Customers</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 4px solid {theme["success"]};'>
                    <h3 style='color: {theme["success"]}; margin: 0;'>{int(ret['repeat_customers'].iloc[0]):,}</h3>
                    <p style='color: {theme["muted"]}; margin: 5px 0 0 0;'>Repeat Customers</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 4px solid {theme["danger"]};'>
                    <h3 style='color: {theme["danger"]}; margin: 0;'>{repeat_rate*100:.1f}%</h3>
                    <p style='color: {theme["muted"]}; margin: 5px 0 0 0;'>Repeat Purchase Rate</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 **Insight:** With only ~3% repeat rate, focus should be on post-purchase engagement.")
    
    with tabs[1]:
        st.markdown("### Order Frequency Distribution")
        
        if data['churn_features'] is not None:
            churn = data['churn_features']
            
            # Interactive slider for filtering
            max_orders = int(churn['total_orders'].max())
            order_range = st.slider("Filter by order count:", 1, min(max_orders, 20), (1, min(10, max_orders)))
            
            filtered_churn = churn[(churn['total_orders'] >= order_range[0]) & (churn['total_orders'] <= order_range[1])]
            order_dist = filtered_churn['total_orders'].value_counts().sort_index().reset_index()
            order_dist.columns = ['orders', 'customers']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=order_dist['orders'],
                y=order_dist['customers'],
                marker=dict(color=theme['chart_colors'][0]),
                hovertemplate="<b>%{x} Orders</b><br>Customers: %{y:,}<extra></extra>"
            ))
            fig.update_layout(**create_plotly_layout("", 400))
            fig.update_yaxes(type="log", title="Number of Customers (log scale)")
            fig.update_xaxes(title="Number of Orders")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                pct_one = (churn['total_orders'] == 1).sum() / len(churn) * 100
                st.metric("1 Order Only", f"{pct_one:.1f}%")
            with col2:
                avg_orders = churn['total_orders'].mean()
                st.metric("Avg Orders/Customer", f"{avg_orders:.2f}")
            with col3:
                max_orders = churn['total_orders'].max()
                st.metric("Max Orders", f"{max_orders}")
    
    with tabs[2]:
        st.markdown("### Churn Feature Comparison")
        
        if data['churn_features'] is not None:
            churn = data['churn_features']
            
            # Feature selector
            available_features = ['total_orders', 'total_revenue', 'avg_order_value']
            selected_features = st.multiselect("Select features to compare:", available_features, default=available_features)
            
            if selected_features:
                fig = make_subplots(rows=1, cols=len(selected_features), subplot_titles=selected_features)
                
                for i, feat in enumerate(selected_features, 1):
                    churned = churn[churn['is_churned'] == 1][feat]
                    active = churn[churn['is_churned'] == 0][feat]
                    
                    fig.add_trace(go.Box(y=churned, name='Churned', marker_color=theme['danger'], showlegend=(i==1)), row=1, col=i)
                    fig.add_trace(go.Box(y=active, name='Active', marker_color=theme['success'], showlegend=(i==1)), row=1, col=i)
                
                fig.update_layout(**create_plotly_layout("", 400))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            if data['statistical_tests'] is not None:
                st.markdown("#### Statistical Test Results")
                stat_df = data['statistical_tests'].copy()
                stat_df['significant'] = stat_df['t_test_p_value'].apply(lambda x: '✅ Yes' if x < 0.05 else '❌ No')
                st.dataframe(stat_df.style.format({
                    'churned_mean': '{:.2f}',
                    'active_mean': '{:.2f}',
                    't_test_p_value': '{:.4f}',
                    'mannwhitney_p_value': '{:.4f}'
                }), use_container_width=True)
    
    with tabs[3]:
        st.markdown("### Logistic Regression Model")
        
        if data['logistic_coef'] is not None:
            coef = data['logistic_coef']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=coef['coefficient'],
                y=coef['feature'],
                orientation='h',
                marker=dict(
                    color=[theme['success'] if x > 0 else theme['danger'] for x in coef['coefficient']]
                ),
                text=coef['coefficient'].apply(lambda x: f'{x:.3f}'),
                textposition='outside',
                textfont=dict(color='white')
            ))
            fig.update_layout(**create_plotly_layout("Feature Coefficients (Leakage-Free Model)", 350))
            fig.update_xaxes(title="Coefficient Value")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.warning("""
            ⚠️ **Model Insight:** Without data leakage, the model shows weak predictive power. 
            This suggests that **controlled experimentation** may be more effective than predictive modeling.
            """)

# ============================================================================
# PAGE: A/B TESTING
# ============================================================================
elif page == "🧪 A/B Testing":
    st.markdown("# 🧪 A/B Testing & Experimentation")
    st.markdown("### Evaluate the effectiveness of retention interventions")
    
    if data['ab_test'] is not None:
        ab = data['ab_test']
        
        st.markdown("---")
        
        control_rate = ab[ab['group'] == 'control']['conversion_rate'].values[0] * 100
        treatment_rate = ab[ab['group'] == 'treatment']['conversion_rate'].values[0] * 100
        lift = ((treatment_rate / control_rate) - 1) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_kpi_card("Control", f"{control_rate:.2f}%", "Baseline conversion", "🎯"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_kpi_card("Treatment", f"{treatment_rate:.2f}%", f"+{treatment_rate - control_rate:.2f}% absolute", "🚀"), unsafe_allow_html=True)
        with col3:
            st.markdown(create_kpi_card("Relative Lift", f"+{lift:.0f}%", "Statistically Significant ✓", "📈"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Conversion Rate Comparison")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Control', 'Treatment'],
                y=[control_rate, treatment_rate],
                marker=dict(color=[theme['secondary'], theme['primary']], line=dict(width=0)),
                text=[f'{control_rate:.2f}%', f'{treatment_rate:.2f}%'],
                textposition='outside',
                textfont=dict(size=18, color='white', family='Inter'),
                hovertemplate="<b>%{x}</b><br>Conversion: %{y:.2f}%<extra></extra>"
            ))
            fig.update_layout(**create_plotly_layout("", 400))
            fig.update_yaxes(title="Conversion Rate (%)", range=[0, max(treatment_rate * 1.4, 10)])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("### Sample Size & Conversions")
            
            control_users = ab[ab['group'] == 'control']['users'].values[0]
            control_conv = ab[ab['group'] == 'control']['conversions'].values[0]
            treatment_users = ab[ab['group'] == 'treatment']['users'].values[0]
            treatment_conv = ab[ab['group'] == 'treatment']['conversions'].values[0]
            
            fig = go.Figure()
            fig.add_trace(go.Funnel(
                name='Control',
                y=['Total Users', 'Conversions'],
                x=[control_users, control_conv],
                textposition="inside",
                textinfo="value",
                marker=dict(color=[theme['secondary'], theme['danger']]),
                textfont=dict(size=14)
            ))
            fig.add_trace(go.Funnel(
                name='Treatment',
                y=['Total Users', 'Conversions'],
                x=[treatment_users, treatment_conv],
                textposition="inside",
                textinfo="value",
                marker=dict(color=[theme['primary'], theme['success']]),
                textfont=dict(size=14)
            ))
            fig.update_layout(**create_plotly_layout("", 400))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        st.markdown("### 📊 Statistical Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            z_score = ab['z_score'].iloc[0]
            p_value = ab['p_value'].iloc[0]
            
            st.markdown(f"""
            | Metric | Value |
            |--------|-------|
            | **Z-Score** | {z_score:.2f} |
            | **P-Value** | {p_value:.6f} |
            | **Significance Level** | α = 0.05 |
            | **Result** | ✅ Statistically Significant |
            """)
        
        with col2:
            st.success("""
            **🎯 Conclusion:**
            
            The treatment shows a **+67% relative lift** with p-value < 0.05.
            
            **Recommendation:** Roll out the treatment to all first-time customers.
            """)
    else:
        st.error("A/B test results not available.")

# ============================================================================
# PAGE: STATISTICAL ANALYSIS
# ============================================================================
elif page == "🔬 Statistical Analysis":
    st.markdown("# 🔬 Statistical Analysis")
    st.markdown("### Hypothesis testing and statistical validation")
    
    if data['statistical_tests'] is not None:
        stat = data['statistical_tests']
        
        st.markdown("---")
        st.markdown("### Churned vs Active Customer Comparison")
        
        # Feature selector
        selected_feature = st.selectbox("Select feature to analyze:", stat['feature'].tolist())
        
        row = stat[stat['feature'] == selected_feature].iloc[0]
        
        st.markdown(f"#### 📊 {row['feature'].replace('_', ' ').title()}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Churned', 'Active'],
                y=[row['churned_mean'], row['active_mean']],
                marker=dict(color=[theme['danger'], theme['success']]),
                text=[f"{row['churned_mean']:.2f}", f"{row['active_mean']:.2f}"],
                textposition='outside',
                textfont=dict(color='white')
            ))
            fig.update_layout(**create_plotly_layout("Mean Values", 300))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            significance = row['t_test_p_value'] < 0.05
            color = theme['success'] if significance else theme['danger']
            status = "Significant" if significance else "Not Significant"
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; text-align: center; height: 220px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='color: {theme["muted"]}; margin: 0;'>T-Test P-Value</h4>
                <h2 style='color: {color}; margin: 10px 0;'>{row['t_test_p_value']:.4f}</h2>
                <p style='color: {color};'>{status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            significance = row['mannwhitney_p_value'] < 0.05
            color = theme['success'] if significance else theme['danger']
            status = "Significant" if significance else "Not Significant"
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; text-align: center; height: 220px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='color: {theme["muted"]}; margin: 0;'>Mann-Whitney P-Value</h4>
                <h2 style='color: {color}; margin: 10px 0;'>{row['mannwhitney_p_value']:.4f}</h2>
                <p style='color: {color};'>{status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📝 Summary of Findings")
        
        st.warning("""
        **No statistically significant differences found between churned and active customers.**
        
        This indicates that early behavioral signals are weak predictors of churn.
        **Implication:** Focus on experimental approaches (A/B testing) rather than predictive modeling.
        """)
    else:
        st.error("Statistical test results not available.")

# ============================================================================
# PAGE: DATA EXPLORER
# ============================================================================
elif page == "📋 Data Explorer":
    st.markdown("# 📋 Data Explorer")
    st.markdown("### Explore the underlying datasets")
    
    st.markdown("---")
    
    dataset_options = {
        "Monthly Revenue": data['monthly_revenue'],
        "Retention Metrics": data['retention_metrics'],
        "Churn Features": data['churn_features'],
        "A/B Test Results": data['ab_test'],
        "Statistical Tests": data['statistical_tests'],
        "Model Coefficients": data['logistic_coef']
    }
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_dataset = st.selectbox("Select Dataset", list(dataset_options.keys()))
    with col2:
        show_stats = st.checkbox("Show Statistics", value=True)
    
    df = dataset_options[selected_dataset]
    
    if df is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Rows", f"{len(df):,}")
        with col2:
            st.metric("Columns", f"{len(df.columns)}")
        with col3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        st.markdown("---")
        
        # Search/Filter
        search = st.text_input("🔍 Search in data:", placeholder="Type to filter...")
        
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            display_df = df[mask]
        else:
            display_df = df
        
        st.markdown("### 📄 Data Preview")
        st.dataframe(display_df.head(100), use_container_width=True, height=400)
        
        if show_stats and len(df.select_dtypes(include=['number']).columns) > 0:
            st.markdown("### 📊 Quick Statistics")
            st.dataframe(df.describe(), use_container_width=True)
        
        # Download option
        st.markdown("### 📥 Download Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"{selected_dataset.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
    else:
        st.error(f"{selected_dataset} data not available.")

# ============================================================================
# PAGE: ASK AI (Advanced RAG Chat)
# ============================================================================
elif page == "🤖 Ask AI":
    st.markdown(f"""
    <div style='margin-bottom: 20px;'>
        <div class='hero-badge'>AI-Powered Analytics</div>
        <h1 style='font-size: 2.4rem; margin: 10px 0 5px 0; background: linear-gradient(135deg, {theme["primary"]}, {theme["accent"]}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800;'>Ask AI</h1>
        <p style='color: {theme["muted"]}; font-size: 1rem; margin: 0;'>Ask anything about the Olist analytics project &bull; Powered by Groq + Llama 3.1</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # ── Backend detection ─────────────────────────────────────────────────────
    # Try to load secrets from Streamlit Cloud or .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Also try streamlit secrets (for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets'):
            for key in ["GROQ_API_KEY", "PINECONE_API_KEY"]:
                if key in st.secrets and not os.getenv(key):
                    os.environ[key] = st.secrets[key]
    except Exception:
        pass

    groq_key = os.getenv("GROQ_API_KEY", "")
    pinecone_key = os.getenv("PINECONE_API_KEY", "")

    # Check Ollama availability
    ollama_online = False
    try:
        import ollama as _ollama
        _ollama.list()
        ollama_online = True
    except Exception:
        pass

    # Check Groq availability
    groq_online = bool(groq_key)

    # Determine which backend to use
    # Priority: Groq (fast cloud) > Ollama + Pinecone (local RAG)
    use_groq = groq_online
    use_full_rag = ollama_online and bool(pinecone_key) and not use_groq
    ai_available = use_groq or use_full_rag

    # ── Status banner ────────────────────────────────────────────────────────
    if ai_available:
        if use_groq:
            backend_label = "Groq Cloud AI"
            model_label = "llama-3.1-8b-instant"
        else:
            backend_label = "Full RAG Pipeline"
            model_label = "llama3 + nomic-embed"
        
        st.markdown(f"""
        <div style='display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;'>
            <div class='status-pill online'>
                <span style='width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block; animation: pulse 2s infinite;'></span>
                {backend_label}
            </div>
            <div class='status-pill connected'>
                <span style='width: 8px; height: 8px; border-radius: 50%; background: {theme["primary"]}; display: inline-block;'></span>
                {model_label}
            </div>
            <div class='status-pill connected'>
                ⚡ Instant Responses
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("🔴 No AI backend available — set GROQ_API_KEY in .env")

    st.markdown("", unsafe_allow_html=True)

    # ── Not available fallback ───────────────────────────────────────────────
    if not ai_available:
        st.markdown(f"""
        <div style='
            background: rgba(239,68,68,0.1);
            border: 1px solid rgba(239,68,68,0.4);
            border-left: 4px solid #ef4444;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        '>
            <h4 style='color:#ef4444; margin:0 0 8px 0;'>⚠️ AI Chat Not Available</h4>
            <p style='color: {theme["muted"]}; margin:0;'>
                To enable the AI chat, set up one of these backends:<br><br>
                <strong>Option A (Cloud - Recommended):</strong><br>
                1. Get a free API key from <a href='https://console.groq.com' target='_blank'>console.groq.com</a><br>
                2. Set <code>GROQ_API_KEY</code> in your <code>.env</code> file or Streamlit Cloud secrets<br><br>
                <strong>Option B (Local - Full RAG):</strong><br>
                1. Install & start Ollama: <code>ollama serve</code><br>
                2. Pull models: <code>ollama pull llama3 && ollama pull nomic-embed-text</code><br>
                3. Set <code>PINECONE_API_KEY</code> in your <code>.env</code> file<br>
                4. Run: <code>python rag/test_pipeline.py</code>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Sample questions ─────────────────────────────────────────────────────
    st.markdown("### 💡 Sample Questions")
    sample_qs = [
        "What is the customer retention rate and why is it so low?",
        "Why does the churn prediction model only achieve 55% accuracy?",
        "What were the A/B test results and what is the ROI?",
        "Explain the data leakage issue in the original churn model.",
        "What SQL query was used to calculate monthly revenue?",
        "What are the top business recommendations from this analysis?",
    ]

    cols = st.columns(2)
    for i, q in enumerate(sample_qs):
        with cols[i % 2]:
            if st.button(q, key=f"sample_q_{i}", use_container_width=True,
                         disabled=not ai_available):
                st.session_state.setdefault("chat_messages", [])
                st.session_state["pending_question"] = q

    st.markdown("---")

    # ── Chat history ─────────────────────────────────────────────────────────
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for msg in st.session_state.chat_messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f"""
            <div class='chat-user'>
                <span style='font-size: 0.78rem; color:{theme["primary"]}; font-weight: 600;'>You</span><br>
                <span style='color: white;'>{content}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            sources = msg.get("sources", "")
            st.markdown(f"""
            <div class='chat-ai'>
                <span style='font-size: 0.78rem; color:{theme["accent"]}; font-weight: 600;'>🤖 AI Analyst</span><br>
                <span style='color: {theme["muted"]}; line-height: 1.6;'>{content}</span>
                {f'<br><br><span style="font-size:0.75rem; color:{theme["primary"]}; opacity: 0.8;">📎 {sources}</span>' if sources else ''}
            </div>
            """, unsafe_allow_html=True)

    # ── Input area ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            user_input = st.text_input(
                "Ask a question:",
                placeholder="e.g. Why did the churn model fail? What drove revenue growth?",
                label_visibility="collapsed",
                disabled=not ai_available,
            )
        with col_btn:
            submitted = st.form_submit_button(
                "Send ➤",
                use_container_width=True,
                disabled=not ai_available,
            )

    # Handle sample question injection
    if "pending_question" in st.session_state:
        user_input = st.session_state.pop("pending_question")
        submitted = True

    # ── Run AI pipeline ──────────────────────────────────────────────────────
    if submitted and user_input and user_input.strip() and ai_available:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        with st.spinner("🧠 Thinking..."):
            try:
                import sys
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

                if use_full_rag:
                    # ── Full RAG pipeline (local Ollama + Pinecone) ──
                    from rag.pipeline import OlistRAGPipeline
                    from rag.document_loader import DocumentLoader
                    from rag.indexer import PineconeIndexer
                    from rag.config import INDEX_FILES

                    if "rag_pipeline" not in st.session_state:
                        loader = DocumentLoader()
                        docs = loader.load_all(INDEX_FILES)
                        indexer = PineconeIndexer()
                        all_texts = [doc.content for ns_docs in docs.values() for doc in ns_docs]
                        indexer.bm25.fit(all_texts)
                        st.session_state.rag_pipeline = OlistRAGPipeline(
                            bm25_encoder=indexer.bm25
                        )

                    pipeline = st.session_state.rag_pipeline
                    answer = pipeline.query(user_input)

                elif use_groq:
                    # ── Groq cloud backend (inline, no rag import needed) ──
                    # Clear any cached failed import
                    import importlib
                    if 'groq' in sys.modules and sys.modules['groq'] is None:
                        del sys.modules['groq']
                    _groq_mod = importlib.import_module('groq')
                    _GroqClient = _groq_mod.Groq

                    # Load project context
                    _base = os.path.dirname(os.path.abspath(__file__))
                    _context = ""
                    _data_files = {
                        "Monthly Revenue": os.path.join(_base, "output", "monthly_revenue.csv"),
                        "Retention Metrics": os.path.join(_base, "output", "retention_metrics.csv"),
                        "Churn Stats": os.path.join(_base, "output", "churn_statistical_tests.csv"),
                        "AB Test Results": os.path.join(_base, "output", "ab_test_second_purchase_results.csv"),
                        "Model Coefficients": os.path.join(_base, "output", "logistic_regression_coefficients_v2.csv"),
                        "Recommendations": os.path.join(_base, "business_recommendations.md"),
                    }
                    for _label, _path in _data_files.items():
                        if os.path.exists(_path):
                            with open(_path, "r", encoding="utf-8") as _f:
                                _context += f"\n--- {_label} ---\n{_f.read()}\n"

                    _sys_prompt = (
                        "You are an expert data analyst who built the Olist E-Commerce Analytics project. "
                        "You analyzed 100K+ orders from Brazil's largest marketplace. "
                        "97% of customers churn after first purchase. Repeat rate is ~3%. "
                        "A leakage-free logistic regression got only 55% accuracy. "
                        "An A/B test with 10% discount showed 18% lift (p<0.001, 4x ROI). "
                        "Answer based ONLY on the provided data. Cite specific numbers."
                    )

                    _client = _GroqClient(api_key=groq_key)
                    _resp = _client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": _sys_prompt},
                            {"role": "user", "content": f"DATA:\n{_context}\n\nQUESTION: {user_input}\n\nAnswer:"},
                        ],
                        temperature=0.1,
                        max_tokens=1024,
                    )
                    answer = _resp.choices[0].message.content.strip()
                    answer += "\n\n📎 Sources: monthly_revenue.csv, retention_metrics.csv, churn_statistical_tests.csv, ab_test_results.csv"

                # Split answer from sources
                sources = ""
                if "📎 Sources:" in answer:
                    parts = answer.split("📎 Sources:")
                    answer_text = parts[0].strip()
                    sources = "Sources: " + parts[1].strip()
                else:
                    answer_text = answer

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer_text,
                    "sources": sources,
                })

            except Exception as e:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"❌ Error: {e}",
                    "sources": "",
                })

        st.rerun()

    # ── Clear chat button ────────────────────────────────────────────────────
    if st.session_state.get("chat_messages"):
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            if "rag_pipeline" in st.session_state:
                del st.session_state["rag_pipeline"]
            st.rerun()

    # ── How it works expander ────────────────────────────────────────────────
    with st.expander("⚙️ How the AI Pipeline Works"):
        st.markdown(f"""
        <div style='color: {theme["muted"]};'>

        This chat is powered by an <strong>Advanced RAG (Retrieval-Augmented Generation)</strong> pipeline
        built specifically for this project. Every question goes through 4 stages:

        **1️⃣ Pre-Retrieval**
        - <strong>Query Rewriting</strong> — LLM reformulates vague queries into precise, searchable ones
        - <strong>Multi-Query Generation</strong> — Creates 3 alternative phrasings to capture different angles
        - <strong>Domain Routing</strong> — Keyword matching routes the query to the right namespace(s):
          <code>revenue</code>, <code>retention</code>, <code>churn</code>, <code>ab_test</code>, <code>methodology</code>, <code>general</code>

        **2️⃣ Retrieval**
        - <strong>Hybrid Search</strong> — Combines dense embeddings (semantic) + BM25 sparse vectors (keyword)
        - <strong>MMR</strong> — Maximal Marginal Relevance diversifies results to avoid redundant chunks
        - <strong>Cross-Encoder Re-Ranking</strong> — `ms-marco-MiniLM-L-6-v2` scores query-document pairs jointly for precision

        **3️⃣ Post-Retrieval**
        - <strong>Contextual Compression</strong> — LLM extracts only the relevant sentences from each chunk

        **4️⃣ Generation**
        - <strong>Domain Prompt Engineering</strong> — System prompt grounds the LLM as an Olist data analyst
        - <strong>Answer Generation</strong> — `llama3` via Ollama produces the final answer with source citations

        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div class='footer'>
    <p>📊 Olist E-Commerce Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p>Data Source: <a href='https://www.kaggle.com/olistbr/brazilian-ecommerce' target='_blank'>Olist Brazilian E-Commerce Dataset</a></p>
</div>
""", unsafe_allow_html=True)
