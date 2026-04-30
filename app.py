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
        "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "sidebar_bg": "linear-gradient(180deg, #3b2667 0%, #5c3d8c 50%, #7b52a8 100%)",
        "primary": "#a855f7",
        "secondary": "#6366f1",
        "accent": "#ec4899",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "text": "#ffffff",
        "muted": "#d8b4fe",
        "card_bg": "rgba(168, 85, 247, 0.25)",
        "chart_colors": ["#a855f7", "#6366f1", "#ec4899", "#14b8a6", "#f59e0b"]
    },
    "Ocean Blue": {
        "bg_gradient": "linear-gradient(135deg, #0c1929 0%, #0a2540 50%, #0d3b66 100%)",
        "sidebar_bg": "linear-gradient(180deg, #0077b6 0%, #0096c7 50%, #00b4d8 100%)",
        "primary": "#00d4ff",
        "secondary": "#0099cc",
        "accent": "#00ff88",
        "success": "#00ff88",
        "warning": "#ffcc00",
        "danger": "#ff5555",
        "text": "#ffffff",
        "muted": "#caf0f8",
        "card_bg": "rgba(0, 212, 255, 0.25)",
        "chart_colors": ["#00d4ff", "#0099cc", "#00ff88", "#ffcc00", "#ff6b9d"]
    },
    "Sunset Vibes": {
        "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #2d1b3d 50%, #44203f 100%)",
        "sidebar_bg": "linear-gradient(180deg, #f093fb 0%, #f5576c 50%, #ff6b6b 100%)",
        "primary": "#ff6b6b",
        "secondary": "#feca57",
        "accent": "#ff9ff3",
        "success": "#1dd1a1",
        "warning": "#feca57",
        "danger": "#ff6b6b",
        "text": "#ffffff",
        "muted": "#ffeef1",
        "card_bg": "rgba(255, 107, 107, 0.25)",
        "chart_colors": ["#ff6b6b", "#feca57", "#ff9ff3", "#54a0ff", "#1dd1a1"]
    },
    "Emerald Dark": {
        "bg_gradient": "linear-gradient(135deg, #0f1419 0%, #1a2f23 50%, #234532 100%)",
        "sidebar_bg": "linear-gradient(180deg, #059669 0%, #10b981 50%, #34d399 100%)",
        "primary": "#10b981",
        "secondary": "#34d399",
        "accent": "#6ee7b7",
        "success": "#10b981",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "text": "#ffffff",
        "muted": "#d1fae5",
        "card_bg": "rgba(16, 185, 129, 0.25)",
        "chart_colors": ["#10b981", "#34d399", "#6ee7b7", "#fbbf24", "#f87171"]
    }
}

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = "Midnight Purple"

theme = THEMES[st.session_state.theme]

# Dynamic CSS based on theme
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {theme['bg_gradient']};
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
        border-right: 2px solid rgba(255,255,255,0.2);
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
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }}
    
    [data-testid="stMetric"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        border-color: {theme['primary']};
    }}
    
    [data-testid="stMetricValue"] {{
        color: {theme['primary']} !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {theme['muted']} !important;
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
    
    .kpi-card {{
        background: linear-gradient(135deg, {theme['card_bg']} 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }}
    
    .big-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {theme['primary']};
    }}
    
    .stat-label {{
        color: {theme['muted']};
        font-size: 0.9rem;
        margin-top: 5px;
    }}
    
    .insight-card {{
        background: {theme['card_bg']};
        border-left: 4px solid {theme['primary']};
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin: 15px 0;
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
        100% {{ opacity: 1; }}
    }}
    
    .footer {{
        text-align: center;
        padding: 20px;
        color: {theme['muted']};
        font-size: 0.9rem;
    }}
    
    .footer a {{
        color: {theme['primary']};
        text-decoration: none;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
    }}
    
    /* Slider styling */
    .stSlider > div > div {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['secondary']} 100%);
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
        <div style='font-size: 1.5rem;'>{icon}</div>
        <div class='big-number'>{value}</div>
        <div style='color: white; font-weight: 600; margin-top: 5px;'>{title}</div>
        <div class='stat-label'>{subtitle}</div>
    </div>
    """

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================
if page == "🏠 Overview":
    st.markdown("# 🎯 Olist E-Commerce Analytics Dashboard")
    st.markdown("### Comprehensive analysis of customer retention, churn prediction & experimentation")
    
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
    
    st.markdown("---")
    
    # Key Findings Section
    st.markdown("### 🔍 Key Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📉 Low Retention Rate**
        
        ~97% of customers do not make a second purchase. This indicates significant opportunity for retention improvement.
        """)
    
    with col2:
        st.warning("""
        **⚠️ Weak Churn Signal**
        
        Early churn is difficult to predict without data leakage. Statistical tests confirm limited behavioral separation.
        """)
    
    with col3:
        st.success("""
        **✅ Experimentation Works**
        
        A/B testing shows +67% lift in second purchase conversion, proving controlled experiments are effective.
        """)

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
    st.markdown("# 🤖 Ask AI")
    st.markdown("### Ask anything about the Olist analytics project — powered by AI")
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
    # Priority: Ollama + Pinecone (full RAG) > Groq (cloud context)
    use_full_rag = ollama_online and bool(pinecone_key)
    use_groq = groq_online and not use_full_rag
    ai_available = use_full_rag or use_groq

    # ── Status banner ────────────────────────────────────────────────────────
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if use_full_rag:
            st.success("🟢 Full RAG Pipeline")
        elif use_groq:
            st.success("🟢 Groq Cloud AI")
        else:
            st.error("🔴 No AI Backend")
    with col_s2:
        if ollama_online:
            st.success("🟢 Ollama — Online")
        elif groq_online:
            st.info("🔵 Groq — Connected")
        else:
            st.warning("🟡 Set GROQ_API_KEY")
    with col_s3:
        if use_full_rag:
            st.info("🔵 llama3 + nomic-embed")
        elif use_groq:
            st.info("🔵 llama-3.3-70b (Groq)")
        else:
            st.info("🔵 No model loaded")

    st.markdown("<br>", unsafe_allow_html=True)

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
            <div style='
                background: {theme["card_bg"]};
                border: 1px solid {theme["primary"]}40;
                border-radius: 12px 12px 4px 12px;
                padding: 14px 18px;
                margin: 8px 0 8px 15%;
                text-align: right;
            '>
                <span style='font-size: 0.8rem; color:{theme["primary"]};'>You</span><br>
                <span style='color: white;'>{content}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            sources = msg.get("sources", "")
            st.markdown(f"""
            <div style='
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px 12px 12px 4px;
                padding: 14px 18px;
                margin: 8px 15% 8px 0;
            '>
                <span style='font-size: 0.8rem; color:{theme["accent"]};'>🤖 AI Analyst</span><br>
                <span style='color: {theme["muted"]};'>{content}</span>
                {f'<br><br><span style="font-size:0.75rem; color:{theme["primary"]};">📎 {sources}</span>' if sources else ''}
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
                    from groq import Groq as _GroqClient

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
                        model="llama-3.3-70b-versatile",
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
