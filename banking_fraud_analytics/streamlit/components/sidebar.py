import streamlit as st
import matplotlib as mpl

THEMES = {
    "🌙 Dark": {
        "bg": "#0F1117",
        "secondary_bg": "#1E2130",
        "text": "#FAFAFA",
        "primary": "#2E86AB",
        "metric_bg": "#1E2130",
        "mpl": {
            'figure.facecolor': '#1E2130',
            'axes.facecolor': '#1E2130',
            'axes.edgecolor': '#AAAAAA',
            'axes.labelcolor': '#FAFAFA',
            'xtick.color': '#FAFAFA',
            'ytick.color': '#FAFAFA',
            'text.color': '#FAFAFA',
            'legend.facecolor': '#1E2130',
            'legend.edgecolor': '#AAAAAA',
            'grid.color': '#2E3250',
            'grid.linestyle': '--',
            'grid.alpha': 0.5,
        }
    },
    "☀️ Light": {
        "bg": "#FFFFFF",
        "secondary_bg": "#F0F2F6",
        "text": "#1E2130",
        "primary": "#2E86AB",
        "metric_bg": "#F0F2F6",
        "mpl": {
            'figure.facecolor': '#FFFFFF',
            'axes.facecolor': '#F8F9FA',
            'axes.edgecolor': '#CCCCCC',
            'axes.labelcolor': '#1E2130',
            'xtick.color': '#1E2130',
            'ytick.color': '#1E2130',
            'text.color': '#1E2130',
            'legend.facecolor': '#FFFFFF',
            'legend.edgecolor': '#CCCCCC',
            'grid.color': '#EEEEEE',
            'grid.linestyle': '--',
            'grid.alpha': 0.5,
        }
    },
    "💻 System": {
        "bg": "#0F1117",
        "secondary_bg": "#1E2130",
        "text": "#FAFAFA",
        "primary": "#2E86AB",
        "metric_bg": "#1E2130",
        "mpl": {}
    }
}

def apply_theme(theme_name):
    theme = THEMES[theme_name]
    mpl.rcParams.update(mpl.rcParamsDefault)
    if theme['mpl']:
        mpl.rcParams.update(theme['mpl'])

    st.markdown(f"""
    <style>
        /* Main background */
        .stApp {{
            background-color: {theme['bg']};
            color: {theme['text']};
        }}
        /* Sidebar background */
        [data-testid="stSidebar"] {{
            background-color: {theme['secondary_bg']};
        }}
        /* Metric cards */
        [data-testid="stMetricValue"] {{
            font-size: 28px;
            font-weight: bold;
            color: {theme['primary']};
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 14px;
            color: {theme['text']};
        }}
        /* All text */
        p, h1, h2, h3, h4, span, label {{
            color: {theme['text']} !important;
        }}
        /* Dataframe */
        [data-testid="stDataFrame"] {{
            background-color: {theme['secondary_bg']};
        }}
        /* Input widgets */
        [data-testid="stSelectbox"] {{
            background-color: {theme['secondary_bg']};
        }}
        /* Page links */
        [data-testid="stSidebarNav"] {{ display: none; }}
        [data-testid="stPageLink"] {{
            background-color: {theme['secondary_bg']};
            border-radius: 8px;
            padding: 5px;
            margin-bottom: 5px;
            width: 100%;
        }}
        [data-testid="stPageLink"]:hover {{
            background-color: {theme['primary']};
            border-radius: 8px;
        }}
        /* Block containers */
        [data-testid="block-container"] {{
            background-color: {theme['bg']};
        }}
        /* Divider */
        hr {{
            border-color: {theme['primary']};
        }}
        /* Header bar */
        [data-testid="stHeader"] {{
            background-color: {theme['bg']};
        }}
        /* Top decoration */
        [data-testid="stDecoration"] {{
            display: none;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <h1 style='color: #2E86AB; font-size: 24px;'>🏦 Banking Fraud</h1>
            <p style='color: #AAAAAA; font-size: 12px;'>Analytics Pipeline</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <div style='padding: 5px;'>
            <h3 style='color: #2E86AB;'>📌 Pages</h3>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_monthly_trends.py", label="📈 Monthly Trends")
        st.page_link("pages/2_fraud_analysis.py", label="🔍 Fraud Analysis")
        st.page_link("pages/3_customer_summary.py", label="👤 Customer Summary")

        st.markdown("---")

        st.markdown("""
        <div style='padding: 5px;'>
            <h3 style='color: #2E86AB;'>⚙️ Pipeline</h3>
            <table style='width:100%; color: #FAFAFA; font-size: 13px;'>
                <tr><td>📦 Source</td><td style='color:#2E86AB'>Kaggle</td></tr>
                <tr><td>🔄 Transform</td><td style='color:#2E86AB'>dbt</td></tr>
                <tr><td>🏗️ Warehouse</td><td style='color:#2E86AB'>Databricks</td></tr>
                <tr><td>📊 Dashboard</td><td style='color:#2E86AB'>Streamlit</td></tr>
                <tr><td>⏰ Orchestrate</td><td style='color:#FFB347'>Airflow soon</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### 🎨 Theme")
        theme = st.selectbox(
            "Select Theme",
            ["🌙 Dark", "☀️ Light", "💻 System"],
            key="theme_selector",
            label_visibility="collapsed"
        )

        st.markdown("---")

        st.markdown("""
        <div style='text-align: center; color: #AAAAAA; font-size: 11px;'>
            Built with ❤️ using<br>dbt + Databricks + Streamlit
        </div>
        """, unsafe_allow_html=True)

    # Apply theme outside sidebar so it affects whole page
    apply_theme(theme)