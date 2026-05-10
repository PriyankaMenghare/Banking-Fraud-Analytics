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

st.set_page_config(page_title="Fraud Analysis", page_icon="🔍", layout="wide")
st.title("🔍 Fraud Analysis Dashboard")

# --- LOAD ALL DATA VIA SQL AGGREGATIONS ---
metrics = run_query("""
    SELECT
        COUNT(*)                                                        AS total_transactions,
        SUM(CASE WHEN is_fraud = 'Yes' THEN 1 ELSE 0 END)             AS total_fraud,
        ROUND(SUM(CASE WHEN is_fraud = 'Yes' THEN 1 ELSE 0 END) * 100.0
              / COUNT(*), 2)                                           AS fraud_rate,
        SUM(CASE WHEN is_compromised = TRUE THEN 1 ELSE 0 END)        AS compromised_cards
    FROM {CATALOG}.gold.gold_fraud_analysis
""")

fraud_flags = run_query("""
    SELECT fraud_flag, COUNT(*) AS count
    FROM {CATALOG}.gold.gold_fraud_analysis
    GROUP BY fraud_flag
    ORDER BY count DESC
""")

card_fraud = run_query("""
    SELECT card_brand, COUNT(*) AS fraud_count
    FROM {CATALOG}.gold.gold_fraud_analysis
    WHERE is_fraud = 'Yes'
    GROUP BY card_brand
    ORDER BY fraud_count DESC
""")

merchant_fraud = run_query("""
    SELECT merchant_category, COUNT(*) AS fraud_count
    FROM {CATALOG}.gold.gold_fraud_analysis
    WHERE is_fraud = 'Yes'
    GROUP BY merchant_category
    ORDER BY fraud_count DESC
    LIMIT 10
""")

direction_fraud = run_query("""
    SELECT transaction_direction, COUNT(*) AS fraud_count
    FROM {CATALOG}.gold.gold_fraud_analysis
    WHERE is_fraud = 'Yes'
    AND transaction_direction != 'zero'
    GROUP BY transaction_direction
""")

credit_score_fraud = run_query("""
    SELECT credit_score_category, COUNT(*) AS fraud_count
    FROM {CATALOG}.gold.gold_fraud_analysis
    WHERE is_fraud = 'Yes'
    GROUP BY credit_score_category
    ORDER BY fraud_count DESC
""")

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Transactions", f"{int(metrics['total_transactions'][0]):,}")
with col2:
    st.metric("Total Fraud", f"{int(metrics['total_fraud'][0]):,}")
with col3:
    st.metric("Fraud Rate", f"{metrics['fraud_rate'][0]}%")
with col4:
    st.metric("Compromised Cards", f"{int(metrics['compromised_cards'][0]):,}")

st.markdown("---")

col1, col2 = st.columns(2)

# --- CHART 1: Fraud Flag Distribution ---
with col1:
    st.subheader("Fraud Flag Distribution")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=fraud_flags, x='count', y='fraud_flag', palette='Reds_r', ax=ax)
    ax.set_xlabel("Count")
    ax.set_ylabel("Fraud Flag")
    plt.tight_layout()
    st.pyplot(fig)

# --- CHART 2: Fraud by Card Brand ---
with col2:
    st.subheader("Fraud by Card Brand")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=card_fraud, x='fraud_count', y='card_brand', palette='Blues_r', ax=ax)
    ax.set_xlabel("Fraud Count")
    ax.set_ylabel("Card Brand")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

col1, col2 = st.columns(2)

# --- CHART 3: Top 10 Merchant Categories by Fraud ---
with col1:
    st.subheader("Top 10 Merchant Categories by Fraud")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(data=merchant_fraud, x='fraud_count', y='merchant_category', palette='Oranges_r', ax=ax)
    ax.set_xlabel("Fraud Count")
    ax.set_ylabel("Merchant Category")
    plt.tight_layout()
    st.pyplot(fig)

# --- CHART 4: Fraud by Credit Score Category ---
with col2:
    st.subheader("Fraud by Credit Score Category")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(data=credit_score_fraud, x='fraud_count', y='credit_score_category', palette='Purples_r', ax=ax)
    ax.set_xlabel("Fraud Count")
    ax.set_ylabel("Credit Score Category")
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# --- CHART 5: Fraud by Transaction Direction ---
st.subheader("Fraud by Transaction Direction")
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=direction_fraud, x='transaction_direction', y='fraud_count', palette='Greens_r', ax=ax)
ax.set_xlabel("Transaction Direction")
ax.set_ylabel("Fraud Count")
plt.tight_layout()
st.pyplot(fig)