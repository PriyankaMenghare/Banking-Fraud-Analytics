# 🏦 Banking Fraud Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.11.7-FF694B?style=flat&logo=dbt&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-3.2.1-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

An end-to-end banking fraud detection and analytics pipeline built with **Databricks**, **dbt**, **Apache Airflow**, and **Streamlit** — processing **13M+ real transactions** through a production-grade Medallion Architecture.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Layers](#data-layers)
- [Fraud Detection Approach](#fraud-detection-approach)
- [Dashboard](#dashboard)
- [Airflow Pipeline](#airflow-pipeline)
- [Setup Guide](#setup-guide)
- [Results](#results)
- [Issues & Solutions](#issues--solutions)
- [Future Improvements](#future-improvements)

---

## 🎯 Project Overview

This project builds a complete data engineering pipeline that:
- Ingests raw banking transaction data into **Databricks Unity Catalog**
- Transforms data through **Bronze → Silver → Gold** layers using **dbt**
- Detects fraudulent transactions using rule-based SQL logic validated against ground-truth labels
- Visualises insights through an interactive **Streamlit** multi-page dashboard
- Automates the entire pipeline on a **daily schedule** using **Apache Airflow** (Dockerised)

### Business Questions Answered
- Which transactions are fraudulent?
- Which customers have the highest fraud risk?
- Which merchant categories have the most fraud?
- What time of day / month do frauds peak?
- What are monthly transaction volume trends?
- How does credit score correlate with fraud rate?

---

## 🏗️ Architecture

```
Kaggle Dataset (CSV files)
        ↓
Databricks Unity Catalog (Raw Storage)
        ↓
dbt Bronze Layer (Raw ingestion + type casting)
        ↓
dbt Silver Layer (Cleaning + enrichment + joins)
        ↓
dbt Gold Layer (Business metrics + fraud detection)
        ↓
Apache Airflow (Daily orchestration @ 6AM UTC)
        ↓
Streamlit Dashboard (Visualisation + insights)
```

---

## 📊 Dataset

**Source:** [Financial Transactions Dataset — Kaggle](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets)

| File | Description | Rows |
|------|-------------|------|
| `transactions_data.csv` | Banking transactions with merchant details | 13M+ |
| `users_data.csv` | Customer demographics and financial info | 1,219 |
| `cards_data.csv` | Card details including dark web flags | — |
| `mcc_codes.json` | Merchant category code lookup (dbt seed) | 109 |
| `train_fraud_labels.json` | Ground truth fraud labels (dbt seed) | 13K+ |

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| **Databricks** | Serverless | Data warehouse + compute |
| **dbt-databricks** | 1.11.7 | Data transformations |
| **Apache Airflow** | 3.2.1 | Pipeline orchestration |
| **Streamlit** | Latest | Interactive dashboard |
| **Seaborn / Matplotlib** | Latest | Visualisations |
| **Docker** | 29.3.0 | Airflow containerisation |
| **uv** | Latest | Python package management |
| **Python** | 3.12 | Primary language |

---

## 📁 Project Structure

```
banking_fraud_analytics/
├── models/
│   ├── bronze/
│   │   ├── source.yml
│   │   ├── schema.yml
│   │   ├── bronze_transactions.sql
│   │   ├── bronze_users.sql
│   │   └── bronze_cards.sql
│   ├── silver/
│   │   ├── schema.yml
│   │   ├── silver_transactions.sql
│   │   ├── silver_users.sql
│   │   └── silver_cards.sql
│   └── gold/
│       ├── schema.yml
│       ├── gold_fraud_analysis.sql
│       ├── gold_customer_summary.sql
│       └── gold_monthly_trends.sql
├── seeds/
│   ├── mcc_codes.csv
│   └── train_fraud_labels.csv
├── macros/
│   └── generate_schema_name.sql
├── tests/
├── analyses/
├── snapshots/
├── streamlit/
│   ├── .streamlit/config.toml
│   ├── components/
│   │   ├── __init__.py
│   │   └── sidebar.py
│   ├── pages/
│   │   ├── 1_monthly_trends.py
│   │   ├── 2_fraud_analysis.py
│   │   └── 3_customer_summary.py
│   ├── app.py
│   └── db_connection.py
├── airflow/
│   ├── dags/
│   │   └── banking_fraud_dag.py
│   ├── .env
│   └── docker-compose.yaml
├── scripts/
│   └── convert_json_to_csv.py
├── data/
│   ├── mcc_codes.json
│   └── train_fraud_labels.json
├── dbt_project.yml
├── pyproject.toml
└── README.md
```

---

## 📦 Data Layers

### 🥉 Bronze — Raw Ingestion
Raw data ingested from source with minimal transformations:
- Type casting (`amount`, `credit_limit`, `income` — removing `$` signs)
- Column renaming for consistency (`id` → `customer_id`, `card_id`, etc.)
- No business logic applied
- Materialised as **tables** in `bronze` schema

### 🥈 Silver — Cleaned & Enriched
Cleaned, validated, and enriched data:
- Date parts extracted (`year`, `month`, `day`, `hour`)
- Transaction direction derived (`debit` / `credit`)
- Fraud labels joined from seed table
- Merchant category descriptions joined from `mcc_codes`
- Credit score categories derived (`Exceptional`, `Very Good`, `Good`, `Fair`, `Poor`)
- Debt-to-income ratio calculated
- Dark web card flag derived (`is_compromised`)
- Materialised as **tables** in `silver` schema

### 🥇 Gold — Business Analytics
Business-ready aggregated tables for dashboards and reporting:

| Model | Description |
|-------|-------------|
| `gold_fraud_analysis` | Transaction-level fraud flags + actual ground-truth labels |
| `gold_customer_summary` | Customer aggregated metrics + fraud rate per customer |
| `gold_monthly_trends` | Monthly transaction volume trends + fraud rate over time |

Materialised as **tables** in `gold` schema.

---

## 🔍 Fraud Detection Approach

Rule-based fraud detection implemented in SQL within dbt Gold models:

```sql
CASE
    WHEN amount > 10000                     THEN 'high_amount'
    WHEN has_error = TRUE                   THEN 'transaction_error'
    WHEN transaction_hour BETWEEN 0 AND 4  THEN 'unusual_hours'
    WHEN is_compromised = TRUE              THEN 'compromised_card'
    WHEN credit_score_category = 'Poor'     THEN 'poor_credit'
    ELSE 'clean'
END AS fraud_flag
```

The `fraud_flag` is compared against `is_fraud` (ground truth labels) to measure rule accuracy.

### Why Rule-Based?

| | Rule-Based (This Project) | ML-Based |
|---|---|---|
| **Explainability** | ✅ Fully transparent | ❌ Black box |
| **Speed to build** | ✅ Fast | ❌ Slow |
| **Accuracy** | Medium | High |
| **Maintenance** | ✅ Easy to update | ❌ Requires retraining |

---

## 📊 Dashboard

Built with **Streamlit** + **Seaborn / Matplotlib**, connected directly to the Gold layer.

### Pages
1. **🏠 Home** — Key metrics: total transactions, fraud count, fraud rate, total customers
2. **📈 Monthly Trends** — Transaction volume & fraud rate over time with year/month filters
3. **🔍 Fraud Analysis** — Fraud breakdown by flag type, card brand, merchant category, credit score
4. **👤 Customer Summary** — Customer spend, fraud rate by age group, gender, credit score tier

### Features
- Dark / Light / System theme toggle
- Year and month filters
- Dual Y-axis charts
- Cached queries (1-hour TTL) for performance

---

## ⏰ Airflow Pipeline

**Schedule:** Daily at 6:00 AM UTC

### DAG: `banking_fraud_analytics`

```
dbt_seed
    ↓
bronze_transactions ──┐
bronze_users          ├── test_bronze
bronze_cards          ┘
    ↓
silver_transactions ──┐
silver_users          ├── test_silver
silver_cards          ┘
    ↓
gold_fraud_analysis ──┐
gold_customer_summary ├── test_gold ── dbt_docs_generate
gold_monthly_trends   ┘
```

- Bronze, Silver, and Gold models each run **in parallel** within their layer
- dbt tests run after **each layer** before proceeding to the next
- dbt docs auto-generated at the end of each successful run

---

## 🚀 Setup Guide

### Prerequisites
- Python 3.12+
- uv package manager
- Docker Desktop
- Databricks workspace
- Kaggle account (for dataset download)

### 1. Clone the repository
```bash
git clone https://github.com/PriyankaMenghare/Banking-Fraud-Analytics
cd Banking-Fraud-Analytics/banking_fraud_analytics
```

### 2. Install dependencies
```bash
uv venv
source .venv/bin/activate
uv add dbt-databricks streamlit databricks-sql-connector pandas seaborn matplotlib python-dotenv
```

### 3. Configure dbt
```bash
# Edit ~/.dbt/profiles.yml with your Databricks credentials
dbt debug  # verify connection
```

### 4. Run the dbt pipeline
```bash
dbt seed                              # load mcc_codes + fraud labels
dbt run                               # run all models (bronze → silver → gold)
dbt test                              # run 28 data quality tests
dbt docs generate && dbt docs serve   # browse model documentation
```

### 5. Run the Streamlit dashboard
```bash
cd streamlit
# Create .env file with your Databricks connection credentials
streamlit run app.py
# Access at http://localhost:8501
```

### 6. Start Airflow
```bash
cd airflow
docker compose up airflow-init
docker compose up -d
# Access Airflow UI at http://localhost:8080  (user: airflow / pass: airflow)
```

---

## 📈 Results

| Metric | Value |
|--------|-------|
| Total Transactions | 13,305,915 |
| Total Customers | 1,219 |
| Total Fraud Transactions | 13,332 |
| Fraud Rate | 0.10% |
| dbt Models | 9 |
| dbt Tests | 28 passing |
| Pipeline Schedule | Daily 6AM UTC |

---

## 🐛 Issues & Solutions

Real problems encountered and resolved during development — documented to help others facing the same stack:

### 1. SSL Certificate Verification Failed
**Error:** `SSLCertVerificationError: certificate verify failed: self signed certificate`  
**Cause:** Corporate proxy / VPN intercepting SSL traffic on Mac.
```bash
pip install --upgrade certifi
# Add to ~/.zshrc:
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$(python3 -c "import certifi; print(certifi.where())")
export NODE_TLS_REJECT_UNAUTHORIZED=0
source ~/.zshrc && code .   # launch VS Code from terminal to inherit env
```

### 2. dbt Power User Extension Queries Hanging
**Cause:** Same SSL issue affecting the VS Code extension's Node.js process.  
**Solution:** Always launch VS Code from terminal after sourcing `~/.zshrc`.

### 3. Databricks SQL Warehouse Cold Start Timeout
**Error:** Queries timing out after 900 seconds.  
**Cause:** Serverless warehouse auto-stopped after inactivity.  
**Solution:** Start the warehouse manually from Databricks UI before running; set auto-stop to 60 minutes during development.

### 4. dbt Manifest Stale (`resolve_ref` error)
**Error:** `AttributeError: 'NoneType' object has no attribute 'resolve_ref'`  
**Cause:** dbt manifest was stale or missing.
```bash
dbt compile  # regenerate manifest.json
# Then: Cmd+Shift+P → "Restart dbt Server"
```

### 5. Custom Schema Not Working (models going to `default`)
**Cause:** Custom macro was named `custom_schema` instead of `generate_schema_name`.  
**Solution:** dbt specifically looks for a macro named `generate_schema_name`. Renaming fixed schema routing to `bronze` / `silver` / `gold`.

### 6. JSON Seeds with Nested Structure
**Error:** `train_fraud_labels.json` converting incorrectly to CSV.  
**Cause:** JSON had a nested dict string `{"target": "{'id': 'No', ...}"}` instead of flat `{"id": "No"}`.  
**Solution:** Used `ast.literal_eval()` to parse the nested string before writing to CSV.

### 7. Docker Volume Mount Path Issue
**Error:** `No dbt_project.yml found at expected path /opt/airflow/dbt/dbt_project.yml`  
**Cause:** Relative path resolving incorrectly in Docker on Mac.
```yaml
# Use absolute path in docker-compose.yaml:
- /Users/priyankamenghare/path/to/banking_fraud_analytics:/opt/airflow/dbt
```

### 8. Airflow OOM Kill on `dbt seed`
**Error:** `Command exited with return code -9` (OOM kill).  
**Cause:** `train_fraud_labels` CSV too large to load via `dbt seed` inside Docker.  
**Solution:** Increased Docker Desktop memory to 6GB; changed DAG to only seed `mcc_codes` since `train_fraud_labels` is already loaded in Databricks.

### 9. Wrong BashOperator Import in Airflow 3.x
**Warning:** `airflow.operators.bash.BashOperator is deprecated`
```python
# Correct import for Airflow 3.x:
from airflow.providers.standard.operators.bash import BashOperator
```

### 10. `profiles.yml` Not Found in Docker Container
**Error:** dbt couldn't find `profiles.yml` inside the Airflow worker container.
```bash
docker exec airflow-airflow-worker-1 mkdir -p /home/airflow/.dbt
docker cp ~/.dbt/profiles.yml airflow-airflow-worker-1:/home/airflow/.dbt/profiles.yml
```

---

## 🔮 Future Improvements

- [ ] Add ML-based fraud scoring using **Databricks MLflow** (XGBoost / LightGBM)
- [ ] Deploy Streamlit dashboard to **Streamlit Cloud** for public access
- [ ] Add **incremental dbt models** for efficient large-table refreshes
- [ ] Add **email alerts** in Airflow on test failures
- [ ] Add **data freshness checks** in dbt source definitions
- [ ] Integrate **Great Expectations** for advanced data quality
- [ ] Add **CI/CD pipeline** with GitHub Actions for automated dbt testing on PRs

---

## 👩‍💻 Author

**Priyanka Ghawghawe**  
Data Analyst & Scientist | Python • SQL • dbt • Airflow • Databricks • Power BI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/priyankaghawghawe/)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/PriyankaMenghare)
[![Email](https://img.shields.io/badge/Email-red?style=flat&logo=gmail)](mailto:priyankamenghare09@gmail.com)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
