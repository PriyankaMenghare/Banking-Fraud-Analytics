import streamlit as st
from db_connection import run_query
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Banking Fraud Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
render_sidebar()

st.markdown("""
<style>
    /* Hide default streamlit page nav */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #2E86AB;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #AAAAAA;
    }
    /* Style page links */
    [data-testid="stPageLink"] {
        background-color: #1E2130;
        border-radius: 8px;
        padding: 5px;
        margin-bottom: 5px;
        width: 100%;
    }
    [data-testid="stPageLink"]:hover {
        background-color: #2E86AB;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🏦 Banking Fraud Analytics")
st.markdown("Real time fraud detection and customer analytics pipeline")
st.markdown("---")

# Load metrics
metrics = run_query("""
    SELECT
        COUNT(transaction_id)                                           AS total_transactions,
        SUM(CASE WHEN is_fraud = 'Yes' THEN 1 ELSE 0 END)             AS total_fraud,
        ROUND(SUM(CASE WHEN is_fraud = 'Yes' THEN 1 ELSE 0 END) * 100.0
              / COUNT(transaction_id), 2)                              AS fraud_rate_pct,
        COUNT(DISTINCT customer_id)                                    AS total_customers
    FROM banking_fraud_analytics_dev.gold.gold_fraud_analysis
""")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💳 Total Transactions", f"{int(metrics['total_transactions'][0]):,}")
with col2:
    st.metric("🚨 Total Fraud", f"{int(metrics['total_fraud'][0]):,}")
with col3:
    st.metric("📊 Fraud Rate", f"{metrics['fraud_rate_pct'][0]}%")
with col4:
    st.metric("👥 Total Customers", f"{int(metrics['total_customers'][0]):,}")

st.markdown("---")

# Quick insights
st.markdown("### 🔎 Quick Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📈 **Monthly Trends**\nAnalyze transaction volume and fraud rate trends over time from 2010 to 2019")

with col2:
    st.warning("🔍 **Fraud Analysis**\nExplore fraud patterns by merchant category, card brand and transaction type")

with col3:
    st.success("👤 **Customer Summary**\nUnderstand customer behavior, spend patterns and risk profiles")