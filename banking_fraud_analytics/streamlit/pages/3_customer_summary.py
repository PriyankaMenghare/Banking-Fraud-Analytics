import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from db_connection import run_query
from components.sidebar import apply_theme, render_sidebar

render_sidebar()
# Apply current theme to charts
theme = st.session_state.get('theme_selector', '🌙 Dark')
apply_theme(theme)

st.set_page_config(page_title="Customer Summary", page_icon="👤", layout="wide")
st.title("👤 Customer Summary Dashboard")

# --- LOAD DATA ---
metrics = run_query("""
    SELECT
        COUNT(DISTINCT customer_id)         AS total_customers,
        ROUND(AVG(total_transactions), 2)   AS avg_transactions,
        ROUND(AVG(total_spend), 2)          AS avg_spend,
        ROUND(AVG(fraud_rate_pct), 2)       AS avg_fraud_rate
    FROM {CATALOG}.gold.gold_customer_summary
""")

spend_by_gender = run_query("""
    SELECT gender,
        COUNT(customer_id)              AS total_customers,
        ROUND(AVG(total_spend), 2)      AS avg_spend,
        ROUND(AVG(fraud_rate_pct), 2)   AS avg_fraud_rate
    FROM {CATALOG}.gold.gold_customer_summary
    GROUP BY gender
""")

spend_by_credit = run_query("""
    SELECT credit_score_category,
        COUNT(customer_id)              AS total_customers,
        ROUND(AVG(total_spend), 2)      AS avg_spend,
        ROUND(AVG(fraud_rate_pct), 2)   AS avg_fraud_rate
    FROM {CATALOG}.gold.gold_customer_summary
    GROUP BY credit_score_category
    ORDER BY avg_fraud_rate DESC
""")

top_fraud_customers = run_query("""
    SELECT customer_id, total_transactions, total_spend,
           total_fraud_transactions, fraud_rate_pct, credit_score_category
    FROM {CATALOG}.gold.gold_customer_summary
    WHERE total_fraud_transactions > 0
    ORDER BY fraud_rate_pct DESC
    LIMIT 10
""")

age_distribution = run_query("""
    SELECT
        CASE
            WHEN current_age < 25 THEN 'Under 25'
            WHEN current_age BETWEEN 25 AND 34 THEN '25-34'
            WHEN current_age BETWEEN 35 AND 44 THEN '35-44'
            WHEN current_age BETWEEN 45 AND 54 THEN '45-54'
            WHEN current_age BETWEEN 55 AND 64 THEN '55-64'
            ELSE '65+'
        END AS age_group,
        COUNT(customer_id)              AS total_customers,
        ROUND(AVG(fraud_rate_pct), 2)   AS avg_fraud_rate
    FROM {CATALOG}.gold.gold_customer_summary
    GROUP BY age_group
    ORDER BY age_group
""")

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", f"{int(metrics['total_customers'][0]):,}")
with col2:
    st.metric("Avg Transactions", f"{metrics['avg_transactions'][0]:,}")
with col3:
    st.metric("Avg Spend", f"${metrics['avg_spend'][0]:,.2f}")
with col4:
    st.metric("Avg Fraud Rate", f"{metrics['avg_fraud_rate'][0]}%")

st.markdown("---")

col1, col2 = st.columns(2)

# --- CHART 1: Avg Spend by Gender ---
with col1:
    st.subheader("Avg Spend by Gender")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=spend_by_gender, x='gender', y='avg_spend', palette='Blues_r', ax=ax)
    ax.set_xlabel("Gender")
    ax.set_ylabel("Avg Spend")
    plt.tight_layout()
    st.pyplot(fig)

# --- CHART 2: Fraud Rate by Credit Score ---
with col2:
    st.subheader("Avg Fraud Rate by Credit Score")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=spend_by_credit, x='avg_fraud_rate', y='credit_score_category', palette='Reds_r', ax=ax)
    ax.set_xlabel("Avg Fraud Rate %")
    ax.set_ylabel("Credit Score Category")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

col1, col2 = st.columns(2)

# --- CHART 3: Customers by Age Group ---
with col1:
    st.subheader("Customers by Age Group")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=age_distribution, x='age_group', y='total_customers', palette='Greens_r', ax=ax)
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Total Customers")
    plt.tight_layout()
    st.pyplot(fig)

# --- CHART 4: Fraud Rate by Age Group ---
with col2:
    st.subheader("Fraud Rate by Age Group")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=age_distribution, x='age_group', y='avg_fraud_rate', palette='Oranges_r', ax=ax)
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Avg Fraud Rate %")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# --- TABLE: Top 10 High Risk Customers ---
st.subheader("🚨 Top 10 High Risk Customers")
st.dataframe(top_fraud_customers, use_container_width=True)