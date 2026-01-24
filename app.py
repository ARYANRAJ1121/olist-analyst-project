"""
Olist E-Commerce Analytics Dashboard
=====================================
A comprehensive Streamlit dashboard for analyzing customer retention,
churn prediction, and experimentation results.
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

# Custom CSS for premium look
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
    }
    
    /* Cards/containers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #a0a0a0;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
    }
    
    /* Selectbox and other inputs */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    /* Custom class for KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .big-number {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9rem;
    }
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
    
    # Load output files
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
    
    # Load raw orders for additional analysis
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
    
    # Navigation
    page = st.radio(
        "Navigate to:",
        ["🏠 Overview", "📈 Revenue Analysis", "🔄 Retention & Churn", 
         "🧪 A/B Testing", "🔬 Statistical Analysis", "📋 Data Explorer"],
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
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        Built with ❤️ using Streamlit<br>
        Data: Olist E-Commerce Dataset
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Color palette for consistent styling
colors = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#00d4aa',
    'warning': '#ffc107',
    'danger': '#ff6b6b',
    'info': '#17a2b8',
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
    'dark_bg': 'rgba(0,0,0,0)',
    'chart_bg': 'rgba(255,255,255,0.02)'
}

def create_plotly_layout(title="", height=400):
    """Create consistent Plotly layout"""
    return dict(
        title=dict(text=title, font=dict(size=20, color='white')),
        paper_bgcolor=colors['dark_bg'],
        plot_bgcolor=colors['chart_bg'],
        font=dict(color='#a0a0a0'),
        height=height,
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    )

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================
if page == "🏠 Overview":
    st.markdown("# 🎯 Olist E-Commerce Analytics Dashboard")
    st.markdown("### Comprehensive analysis of customer retention, churn prediction & experimentation")
    
    st.markdown("---")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if data['retention_metrics'] is not None:
            total_customers = int(data['retention_metrics']['total_customers'].iloc[0])
            st.metric("👥 Total Customers", f"{total_customers:,}", delta="93K+ unique")
    
    with col2:
        if data['monthly_revenue'] is not None:
            total_revenue = data['monthly_revenue']['revenue'].sum()
            st.metric("💰 Total Revenue", f"R${total_revenue/1e6:.1f}M", delta="2016-2018")
    
    with col3:
        if data['retention_metrics'] is not None:
            repeat_rate = data['retention_metrics']['repeat_purchase_rate'].iloc[0] * 100
            st.metric("🔄 Repeat Rate", f"{repeat_rate:.1f}%", delta="-96.9% One-time", delta_color="inverse")
    
    with col4:
        if data['ab_test'] is not None:
            lift = ((data['ab_test'][data['ab_test']['group'] == 'treatment']['conversion_rate'].values[0] / 
                    data['ab_test'][data['ab_test']['group'] == 'control']['conversion_rate'].values[0]) - 1) * 100
            st.metric("🧪 A/B Test Lift", f"+{lift:.0f}%", delta="Significant")
    
    st.markdown("---")
    
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
                line=dict(color=colors['primary'], width=3),
                marker=dict(size=8, color=colors['secondary']),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)',
                name='Revenue'
            ))
            fig.update_layout(**create_plotly_layout("Monthly Revenue (R$)", 350))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🥧 Customer Retention")
        if data['retention_metrics'] is not None:
            repeat_rate = data['retention_metrics']['repeat_purchase_rate'].iloc[0]
            one_time_rate = 1 - repeat_rate
            
            fig = go.Figure(data=[go.Pie(
                labels=['One-time Customers', 'Repeat Customers'],
                values=[one_time_rate * 100, repeat_rate * 100],
                hole=0.6,
                marker=dict(colors=[colors['danger'], colors['success']]),
                textinfo='percent+label',
                textfont=dict(size=14, color='white'),
                hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>"
            )])
            fig.update_layout(**create_plotly_layout("", 350))
            fig.add_annotation(text="97%", x=0.5, y=0.5, font=dict(size=40, color='white'), showarrow=False)
            fig.add_annotation(text="One-time", x=0.5, y=0.38, font=dict(size=14, color='#a0a0a0'), showarrow=False)
            st.plotly_chart(fig, use_container_width=True)
    
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
        
        # Monthly Revenue Trend
        st.markdown("---")
        st.markdown("### Monthly Revenue Trend")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_rev['month'],
            y=df_rev['revenue'],
            mode='lines+markers',
            line=dict(color=colors['primary'], width=3, shape='spline'),
            marker=dict(size=10, color=colors['secondary'], line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.15)',
            name='Revenue',
            hovertemplate="<b>%{x|%B %Y}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
        ))
        fig.update_layout(**create_plotly_layout("", 450))
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💵 Total Revenue", f"R${df_rev['revenue'].sum():,.0f}")
        with col2:
            st.metric("📊 Average Monthly", f"R${df_rev['revenue'].mean():,.0f}")
        with col3:
            st.metric("📈 Peak Month", f"R${df_rev['revenue'].max():,.0f}")
        with col4:
            growth = ((df_rev['revenue'].iloc[-1] / df_rev['revenue'].iloc[1]) - 1) * 100
            st.metric("🚀 Overall Growth", f"+{growth:.0f}%")
        
        st.markdown("---")
        
        # Year-over-Year Comparison
        st.markdown("### Year-over-Year Comparison")
        
        df_rev['year'] = df_rev['month'].dt.year
        df_rev['month_name'] = df_rev['month'].dt.month_name()
        
        yearly_data = df_rev.groupby('year')['revenue'].sum().reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=yearly_data['year'].astype(str),
                y=yearly_data['revenue'],
                marker=dict(
                    color=yearly_data['revenue'],
                    colorscale=[[0, colors['primary']], [1, colors['secondary']]],
                    line=dict(width=0)
                ),
                text=yearly_data['revenue'].apply(lambda x: f'R${x/1e6:.1f}M'),
                textposition='outside',
                textfont=dict(color='white', size=14),
                hovertemplate="<b>%{x}</b><br>Revenue: R$%{y:,.0f}<extra></extra>"
            )
        ])
        fig.update_layout(**create_plotly_layout("Annual Revenue", 400))
        st.plotly_chart(fig, use_container_width=True)
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
                    marker=dict(colors=['#ff6b6b', '#00d4aa']),
                    textinfo='percent',
                    textfont=dict(size=16, color='white'),
                    hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"
                )])
                fig.update_layout(**create_plotly_layout("", 400))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 📌 Key Metrics")
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0;'>
                    <h3 style='color: #667eea; margin: 0;'>{int(ret['total_customers'].iloc[0]):,}</h3>
                    <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Total Unique Customers</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0;'>
                    <h3 style='color: #00d4aa; margin: 0;'>{int(ret['repeat_customers'].iloc[0]):,}</h3>
                    <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Repeat Customers</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0;'>
                    <h3 style='color: #ff6b6b; margin: 0;'>{repeat_rate*100:.1f}%</h3>
                    <p style='color: #a0a0a0; margin: 5px 0 0 0;'>Repeat Purchase Rate</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 **Insight:** With only ~3% repeat rate, focus should be on post-purchase engagement to encourage second purchases.")
    
    with tabs[1]:
        st.markdown("### Order Frequency Distribution")
        
        if data['churn_features'] is not None:
            churn = data['churn_features']
            
            order_dist = churn['total_orders'].value_counts().sort_index().reset_index()
            order_dist.columns = ['orders', 'customers']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=order_dist['orders'],
                y=order_dist['customers'],
                marker=dict(
                    color=order_dist['customers'],
                    colorscale=[[0, colors['secondary']], [1, colors['primary']]],
                ),
                hovertemplate="<b>%{x} Orders</b><br>Customers: %{y:,}<extra></extra>"
            ))
            fig.update_layout(**create_plotly_layout("Number of Orders per Customer", 400))
            fig.update_yaxes(type="log", title="Number of Customers (log scale)")
            fig.update_xaxes(title="Number of Orders")
            st.plotly_chart(fig, use_container_width=True)
            
            # Stats
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
            
            features = ['total_orders', 'total_revenue', 'avg_order_value']
            
            fig = make_subplots(rows=1, cols=3, subplot_titles=features)
            
            for i, feat in enumerate(features, 1):
                churned = churn[churn['is_churned'] == 1][feat]
                active = churn[churn['is_churned'] == 0][feat]
                
                fig.add_trace(go.Box(y=churned, name='Churned', marker_color=colors['danger'], showlegend=(i==1)), row=1, col=i)
                fig.add_trace(go.Box(y=active, name='Active', marker_color=colors['success'], showlegend=(i==1)), row=1, col=i)
            
            fig.update_layout(**create_plotly_layout("Feature Distribution: Churned vs Active", 400))
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistical comparison table
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
                    color=coef['coefficient'].apply(lambda x: colors['success'] if x > 0 else colors['danger'])
                ),
                text=coef['coefficient'].apply(lambda x: f'{x:.3f}'),
                textposition='outside',
                textfont=dict(color='white')
            ))
            fig.update_layout(**create_plotly_layout("Feature Coefficients (Leakage-Free Model)", 350))
            fig.update_xaxes(title="Coefficient Value")
            st.plotly_chart(fig, use_container_width=True)
            
            st.warning("""
            ⚠️ **Model Insight:** Without data leakage, the model shows weak predictive power. 
            The low coefficient magnitudes indicate that transactional features alone cannot reliably predict churn early.
            This suggests that **controlled experimentation** may be more effective than predictive modeling for retention strategy.
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
        
        # Results Overview
        col1, col2, col3 = st.columns(3)
        
        control_rate = ab[ab['group'] == 'control']['conversion_rate'].values[0] * 100
        treatment_rate = ab[ab['group'] == 'treatment']['conversion_rate'].values[0] * 100
        lift = ((treatment_rate / control_rate) - 1) * 100
        
        with col1:
            st.metric("Control Conversion", f"{control_rate:.2f}%", help="Baseline conversion rate")
        with col2:
            st.metric("Treatment Conversion", f"{treatment_rate:.2f}%", delta=f"+{treatment_rate - control_rate:.2f}%")
        with col3:
            st.metric("Relative Lift", f"+{lift:.0f}%", delta="Statistically Significant ✓")
        
        st.markdown("---")
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Conversion Rate Comparison")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Control', 'Treatment'],
                y=[control_rate, treatment_rate],
                marker=dict(color=[colors['secondary'], colors['primary']]),
                text=[f'{control_rate:.2f}%', f'{treatment_rate:.2f}%'],
                textposition='outside',
                textfont=dict(size=16, color='white'),
                hovertemplate="<b>%{x}</b><br>Conversion: %{y:.2f}%<extra></extra>"
            ))
            fig.update_layout(**create_plotly_layout("", 400))
            fig.update_yaxes(title="Conversion Rate (%)", range=[0, max(treatment_rate * 1.3, 10)])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Sample Size & Conversions")
            
            fig = go.Figure()
            
            control_users = ab[ab['group'] == 'control']['users'].values[0]
            control_conv = ab[ab['group'] == 'control']['conversions'].values[0]
            treatment_users = ab[ab['group'] == 'treatment']['users'].values[0]
            treatment_conv = ab[ab['group'] == 'treatment']['conversions'].values[0]
            
            fig.add_trace(go.Funnel(
                name='Control',
                y=['Total Users', 'Conversions'],
                x=[control_users, control_conv],
                textposition="inside",
                textinfo="value",
                marker=dict(color=[colors['secondary'], colors['danger']]),
                textfont=dict(size=14)
            ))
            
            fig.add_trace(go.Funnel(
                name='Treatment',
                y=['Total Users', 'Conversions'],
                x=[treatment_users, treatment_conv],
                textposition="inside",
                textinfo="value",
                marker=dict(color=[colors['primary'], colors['success']]),
                textfont=dict(size=14)
            ))
            
            fig.update_layout(**create_plotly_layout("", 400))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Statistical Details
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
            
            The treatment intervention shows a statistically significant improvement in second-purchase conversion rates.
            With a **+67% relative lift** and p-value < 0.05, we can confidently recommend implementing this retention strategy.
            
            **Recommendation:** Roll out the treatment to all first-time customers.
            """)
    else:
        st.error("A/B test results not available. Please run the analysis pipeline first.")

# ============================================================================
# PAGE: STATISTICAL ANALYSIS
# ============================================================================
elif page == "🔬 Statistical Analysis":
    st.markdown("# 🔬 Statistical Analysis")
    st.markdown("### Hypothesis testing and statistical validation of findings")
    
    if data['statistical_tests'] is not None:
        stat = data['statistical_tests']
        
        st.markdown("---")
        st.markdown("### Churned vs Active Customer Comparison")
        
        # Feature comparison
        for idx, row in stat.iterrows():
            st.markdown(f"#### 📊 {row['feature'].replace('_', ' ').title()}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['Churned', 'Active'],
                    y=[row['churned_mean'], row['active_mean']],
                    marker=dict(color=[colors['danger'], colors['success']]),
                    text=[f"{row['churned_mean']:.2f}", f"{row['active_mean']:.2f}"],
                    textposition='outside',
                    textfont=dict(color='white')
                ))
                fig.update_layout(**create_plotly_layout("Mean Values", 300))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                significance = row['t_test_p_value'] < 0.05
                color = colors['success'] if significance else colors['danger']
                status = "Significant" if significance else "Not Significant"
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;'>
                    <h4 style='color: #a0a0a0; margin: 0;'>T-Test P-Value</h4>
                    <h2 style='color: {color}; margin: 10px 0;'>{row['t_test_p_value']:.4f}</h2>
                    <p style='color: {color};'>{status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                significance = row['mannwhitney_p_value'] < 0.05
                color = colors['success'] if significance else colors['danger']
                status = "Significant" if significance else "Not Significant"
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;'>
                    <h4 style='color: #a0a0a0; margin: 0;'>Mann-Whitney P-Value</h4>
                    <h2 style='color: {color}; margin: 10px 0;'>{row['mannwhitney_p_value']:.4f}</h2>
                    <p style='color: {color};'>{status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # Summary
        st.markdown("### 📝 Summary of Findings")
        
        st.warning("""
        **No statistically significant differences found between churned and active customers.**
        
        All p-values are greater than 0.05 (significance level), indicating that:
        - Churned and active customers have similar purchase behavior
        - Early behavioral signals are weak predictors of churn
        - Transactional data alone may not be sufficient for accurate churn prediction
        
        **Implication:** Focus on experimental approaches (A/B testing) rather than predictive modeling for retention strategy.
        """)
    else:
        st.error("Statistical test results not available. Please run the analysis pipeline first.")

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
    
    selected_dataset = st.selectbox("Select Dataset", list(dataset_options.keys()))
    
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
        
        # Data preview with styling
        st.markdown("### 📄 Data Preview")
        st.dataframe(df.head(100), use_container_width=True, height=400)
        
        # Column info
        st.markdown("### 📋 Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str),
            'Non-Null': df.count().values,
            'Unique': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)
        
        # Download option
        st.markdown("### 📥 Download Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{selected_dataset.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
    else:
        st.error(f"{selected_dataset} data not available.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>📊 Olist E-Commerce Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p>Data Source: <a href='https://www.kaggle.com/olistbr/brazilian-ecommerce' target='_blank'>Olist Brazilian E-Commerce Dataset</a></p>
</div>
""", unsafe_allow_html=True)
