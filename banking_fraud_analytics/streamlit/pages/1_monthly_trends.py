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

st.set_page_config(page_title="Monthly Trends", page_icon="📈", layout="wide")
st.title("📈 Monthly Transaction Trends")

df = run_query("""
    SELECT *
    FROM {CATALOG}.gold.gold_monthly_trends
    ORDER BY transaction_year, transaction_month
""")

df['month_year'] = df['transaction_month'].astype(str) + '/' + df['transaction_year'].astype(str)

# --- FILTERS ---
col1, col2 = st.columns(2)
with col1:
    years = sorted(df['transaction_year'].unique().tolist())
    selected_years = st.multiselect("Filter by Year", years, default=years)
with col2:
    months = sorted(df['transaction_month'].unique().tolist())
    selected_months = st.multiselect("Filter by Month", months, default=months)

df_filtered = df[
    (df['transaction_year'].isin(selected_years)) &
    (df['transaction_month'].isin(selected_months))
]

# --- METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Transactions", f"{int(df_filtered['total_transactions'].sum()):,}")
with col2:
    st.metric("Total Amount", f"${df_filtered['total_amount'].sum():,.2f}")
with col3:
    st.metric("Avg Fraud Rate", f"{df_filtered['fraud_rate_pct'].mean():.2f}%")

st.markdown("---")

tick_positions = range(0, len(df_filtered), max(1, len(df_filtered)//10))
tick_labels = [df_filtered['month_year'].iloc[i] for i in tick_positions]

# --- CHART 1: Transaction Volume + Fraud Rate (Dual Y Axis) ---
st.subheader("Transaction Volume & Fraud Rate Over Time")
fig, ax1 = plt.subplots(figsize=(14, 5))

sns.lineplot(data=df_filtered, x='month_year', y='total_transactions',
             marker='o', color='steelblue', label='Total Transactions', ax=ax1)
ax1.set_ylabel("Total Transactions", color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.set_xticks(tick_labels)
ax1.set_xticklabels(tick_labels, rotation=45, ha='right')

ax2 = ax1.twinx()
sns.lineplot(data=df_filtered, x='month_year', y='fraud_rate_pct',
             marker='o', color='red', label='Fraud Rate %', ax=ax2)
ax2.set_ylabel("Fraud Rate %", color='red')
ax2.tick_params(axis='y', labelcolor='red')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax2.get_legend().remove()

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# --- CHART 2: Debits vs Credits (Dual Y Axis) ---
st.subheader("Total Debits vs Credits Over Time")
fig, ax1 = plt.subplots(figsize=(14, 5))

sns.lineplot(data=df_filtered, x='month_year', y='total_credits',
             marker='o', color='orange', label='Credits', ax=ax1)
ax1.set_ylabel("Credits", color='orange')
ax1.tick_params(axis='y', labelcolor='orange')
ax1.set_xticks(tick_labels)
ax1.set_xticklabels(tick_labels, rotation=45, ha='right')

ax2 = ax1.twinx()
sns.lineplot(data=df_filtered, x='month_year', y='total_debits',
             marker='o', color='steelblue', label='Debits', ax=ax2)
ax2.set_ylabel("Debits", color='steelblue')
ax2.tick_params(axis='y', labelcolor='steelblue')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax2.get_legend().remove()

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# --- RAW DATA ---
with st.expander("View Raw Data"):
    st.dataframe(df_filtered)