# 🏦 Banking Fraud Analytics Pipeline
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.11.7-FF694B?style=flat&logo=dbt&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-3.2.1-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

> An end-to-end data engineering project that detects fraudulent banking transactions using **Databricks**, **dbt**, **Apache Airflow**, and **Streamlit**.

## 🌐 Live Demo
👉 [View Dashboard](https://priyankamenghare-banking-fraud-analytics.streamlit.app)

---

## 📖 Table of Contents

1. [What is this project?](#what-is-this-project)
2. [Key Concepts for Beginners](#key-concepts-for-beginners)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Dataset](#dataset)
6. [Project Structure](#project-structure)
7. [Data Layers Explained](#data-layers-explained)
8. [Fraud Detection Approach](#fraud-detection-approach)
9. [Streamlit Dashboard](#streamlit-dashboard)
10. [Airflow Pipeline](#airflow-pipeline)
11. [CI/CD Pipeline](#cicd-pipeline)
12. [Setup Guide](#setup-guide)
13. [Environment Variables](#environment-variables)
14. [Issues & Solutions](#issues--solutions)
15. [Project Results](#project-results)
16. [Future Improvements](#future-improvements)

---

## 🎯 What is this project?

This project builds a **complete data engineering pipeline** for a bank. It:

- Takes raw banking transaction data (CSV files from Kaggle)
- Stores it in **Databricks** (a cloud data warehouse)
- Transforms it using **dbt** (a SQL transformation tool)
- Detects fraudulent transactions using **SQL rules**
- Visualizes everything in a **Streamlit dashboard**
- Automates the entire process daily using **Apache Airflow**
- Runs automated tests on every code push via **GitHub Actions**

### Business Questions We Answer:
- Which transactions are fraudulent?
- Which customers have the highest fraud risk?
- Which merchant categories have the most fraud?
- What time of day do frauds happen most?
- What are the monthly transaction trends?
- How does credit score relate to fraud rate?

---

## 📚 Key Concepts for Beginners

### 🗄️ What is a Data Warehouse?
A data warehouse is a central place where large amounts of data is stored and organized for analysis. Think of it like a very large, organized filing cabinet for data. Unlike regular databases (used for apps), data warehouses are optimized for running analytical queries on millions of rows.

### 🧱 What is Databricks?
Databricks is a cloud platform built on top of Apache Spark. It provides:
- **Unity Catalog** — organizes data into catalogs → schemas → tables
- **SQL Warehouse** — compute engine to run SQL queries
- **Delta Lake** — storage format for tables (like a supercharged CSV)
- **Notebooks** — interactive Python/SQL environment

### 🔄 What is dbt (data build tool)?
dbt lets data engineers write **SELECT statements** to transform data. You write SQL, dbt handles everything else — running queries, creating tables, testing data quality, and generating documentation.

dbt only handles the **T in ELT** (Extract, Load, Transform).

**Key dbt concepts:**

| Concept | Definition |
|---------|-----------|
| **Model** | A `.sql` file with a SELECT statement that creates a table or view |
| **Source** | A declaration of raw tables that already exist in your warehouse |
| **Seed** | A small CSV file loaded directly into your warehouse via `dbt seed` |
| **Test** | A validation rule that checks data quality |
| **Macro** | A reusable Jinja function (like a helper function in SQL) |
| **Materialization** | How dbt builds a model: `table`, `view`, `incremental`, or `ephemeral` |
| **Incremental** | Only processes new/changed rows — much faster for large tables |
| **ref()** | References another model: `{{ ref('bronze_transactions') }}` |
| **source()** | References raw source data: `{{ source('banking_source', 'transactions_data') }}` |
| **target** | The environment you're running in (dev or prod) |
| **Lineage** | The dependency graph showing how data flows from source to final tables |

### 🥉🥈🥇 What is the Bronze/Silver/Gold Architecture?
Also called the **Medallion Architecture**:

| Layer | Purpose | Data Quality |
|-------|---------|--------------|
| **Bronze** | Store raw data as-is, minimal changes | Low — mirrors source |
| **Silver** | Clean, standardize, enrich data | Medium — validated |
| **Gold** | Final analytics-ready tables | High — trusted |

### 🌱 What are dbt Seeds?
Seeds are small, static CSV files that live inside your dbt project and get loaded into your warehouse with `dbt seed`. Perfect for lookup tables that rarely change.

> **Note:** `train_fraud_labels.csv` in the repo is a **sample** (20 rows) for CI purposes only. Run `python scripts/convert_json_to_csv.py` locally to generate the full dataset before running `dbt seed` in production.

### ✈️ What is Apache Airflow?
Airflow is a workflow orchestration tool that schedules and monitors data pipelines.

| Concept | Definition |
|---------|-----------|
| **DAG** | A collection of tasks organized in a specific order |
| **Task** | A single unit of work (e.g. run a dbt model) |
| **Operator** | Defines what a task does (e.g. BashOperator runs a shell command) |
| **Schedule** | When the DAG runs (e.g. `0 6 * * *` = every day at 6am) |
| **LocalExecutor** | Single-machine execution — no Redis/Celery needed |

### 🔢 What is ELT vs ETL?
- **ETL** — transform data before loading into warehouse
- **ELT** — load raw data first, then transform inside warehouse (modern approach — what we use)

---

## 🛠️ Tech Stack

| Tool | Version | Role |
|------|---------|------|
| **Databricks** | Serverless | Data warehouse + compute |
| **dbt-databricks** | 1.11.8 | SQL transformations |
| **Apache Airflow** | 3.2.1 | Pipeline orchestration |
| **Streamlit** | Latest | Dashboard |
| **Seaborn/Matplotlib** | Latest | Charts |
| **Docker** | 29.3.0 | Airflow containerization |
| **uv** | Latest | Python package management |
| **Python** | 3.12 | Primary language |
| **dbt_utils** | 1.3.0 | dbt helper macros |
| **dbt_expectations** | 0.10.4 | Advanced column-level tests |
| **GitHub Actions** | Latest | CI/CD automation |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                          │
│         Kaggle CSV Files (transactions, users, cards)    │
└─────────────────────┬───────────────────────────────────┘
                      │ Manual upload to Databricks
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   DATABRICKS                             │
│              Unity Catalog Storage                       │
│         {catalog}.source (raw tables)                    │
└─────────────────────┬───────────────────────────────────┘
                      │ dbt reads source tables
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    DBT PIPELINE                          │
│                                                          │
│  Bronze Layer         Silver Layer        Gold Layer     │
│  {catalog}.bronze     {catalog}.silver    {catalog}.gold │
│                                                          │
│  bronze_transactions → silver_transactions → gold_fraud  │
│  bronze_users        → silver_users        → gold_cust   │
│  bronze_cards        → silver_cards        → gold_trends │
│                                                          │
│  Seeds: {catalog}.seeds                                  │
│  mcc_codes, train_fraud_labels                           │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐    ┌─────────────────────┐
│    AIRFLOW      │    │     STREAMLIT        │
│  Runs pipeline  │    │  Reads gold tables   │
│  daily at 6am   │    │  Live dashboard      │
└─────────────────┘    └─────────────────────┘
          ▲
┌─────────────────┐
│  GitHub Actions │
│  CI on push     │
│  dbt test       │
└─────────────────┘
```

---

## 📊 Dataset

**Source:** [Financial Transactions Dataset — Kaggle](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets)

Synthetic banking dataset simulating one bank's operations.

| File | Type | Description | Rows |
|------|------|-------------|------|
| `transactions_data.csv` | Source | Banking transactions | 13M+ |
| `users_data.csv` | Source | Customer demographics | 1,219 |
| `cards_data.csv` | Source | Card details | ~5K |
| `mcc_codes.json` | Seed | Merchant Category Code lookup | 109 |
| `train_fraud_labels.json` | Seed | Ground truth fraud labels | 8.9M |

### Key Columns in `transactions_data`:

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | Unique transaction ID |
| `date` | timestamp | Transaction date and time |
| `client_id` | bigint | Customer ID |
| `card_id` | bigint | Card used |
| `amount` | string | Amount (negative = debit) |
| `use_chip` | string | Chip/Swipe/Online Transaction |
| `mcc` | bigint | Merchant Category Code |
| `errors` | string | Transaction errors (NULL if none) |

---

## 📁 Project Structure

```
Banking-Fraud-Analytics/
├── .gitignore
├── .github/
│   └── workflows/
│       └── dbt_ci.yml              # GitHub Actions CI pipeline
├── README.md
├── pyproject.toml
└── banking_fraud_analytics/
    ├── .env                        # 🔒 Local secrets (NEVER commit!)
    ├── dbt_project.yml             # dbt project configuration
    ├── packages.yml                # dbt packages
    ├── package-lock.yml            # dbt packages lock file
    │
    ├── models/
    │   ├── source/
    │   │   └── source.yml          # Raw source declarations (dynamic catalog)
    │   ├── bronze/
    │   │   ├── schema.yml
    │   │   ├── bronze_transactions.sql  # Incremental model
    │   │   ├── bronze_users.sql
    │   │   └── bronze_cards.sql
    │   ├── silver/
    │   │   ├── schema.yml
    │   │   ├── silver_transactions.sql  # Incremental model
    │   │   ├── silver_users.sql
    │   │   └── silver_cards.sql
    │   └── gold/
    │       ├── schema.yml
    │       ├── gold_fraud_analysis.sql  # Incremental model
    │       ├── gold_customer_summary.sql
    │       └── gold_monthly_trends.sql
    │
    ├── seeds/
    │   ├── mcc_codes.csv           # Full lookup table (109 rows)
    │   └── train_fraud_labels.csv  # Sample for CI (20 rows) — full data generated locally
    │
    ├── macros/
    │   └── generate_schema_name.sql  # Custom schema naming (no target suffix)
    │
    ├── json_data/
    │   ├── mcc_codes.json
    │   └── train_fraud_labels.json
    │
    ├── scripts/
    │   └── convert_json_to_csv.py  # Auto-generates seed CSVs from JSON
    │
    ├── streamlit/
    │   ├── .streamlit/
    │   │   └── config.toml         # Theme configuration
    │   ├── components/
    │   │   ├── __init__.py
    │   │   └── sidebar.py          # Shared navigation + theme
    │   ├── pages/
    │   │   ├── 1_monthly_trends.py
    │   │   ├── 2_fraud_analysis.py
    │   │   └── 3_customer_summary.py
    │   ├── app.py                  # Home page
    │   ├── db_connection.py        # Databricks connection (dynamic catalog)
    │   └── requirements.txt        # Streamlit Cloud dependencies
    │
    ├── airflow/
    │   ├── dags/
    │   │   └── banking_fraud_dag.py  # 14-task decomposed DAG
    │   └── docker-compose.yaml       # Portable with env var paths
    │
    ├── analyses/
    ├── tests/
    └── snapshots/
```

---

## 📦 Data Layers Explained

### 🥉 Bronze Layer — Raw Ingestion

**What we do:**
- Remove `$` signs from monetary columns → cast to `DECIMAL(18,2)`
- Rename columns for consistency (`id` → `transaction_id`)
- `bronze_transactions` is **incremental** (13M+ rows)
- `bronze_users` and `bronze_cards` are **table** (small, no date column)

### 🥈 Silver Layer — Cleaned & Enriched

**What we do:**
- Extract date parts (`year`, `month`, `day`, `hour`)
- Derive `transaction_direction` (`debit`/`credit`) from amount sign
- Join `mcc_codes` for human-readable merchant categories
- Join `train_fraud_labels` for actual fraud labels
- Derive `credit_score_category` (Exceptional/Very Good/Good/Fair/Poor)
- Calculate `debt_to_income_ratio`
- `silver_transactions` is **incremental**

### 🥇 Gold Layer — Business Analytics

| Model | Description | Materialization |
|-------|-------------|----------------|
| `gold_fraud_analysis` | Transaction-level fraud flags + labels | Incremental |
| `gold_customer_summary` | Per-customer aggregated metrics | Table |
| `gold_monthly_trends` | Monthly transaction + fraud trends | Table |

---

## 🔍 Fraud Detection Approach

### Rule-Based Detection

```sql
CASE
    WHEN amount > 10000                      THEN 'high_amount'
    WHEN has_error = TRUE                    THEN 'transaction_error'
    WHEN transaction_hour BETWEEN 0 AND 4   THEN 'unusual_hours'
    WHEN is_compromised = TRUE               THEN 'compromised_card'
    WHEN credit_score_category = 'Poor'      THEN 'poor_credit'
    ELSE 'clean'
END AS fraud_flag
```

| Approach | Rule-Based (Ours) | Machine Learning |
|----------|-------------------|-----------------|
| **Explainability** | ✅ Very clear | ❌ Black box |
| **Speed to build** | ✅ Fast | ❌ Weeks |
| **Accuracy** | Medium | High |
| **Maintenance** | ✅ Easy | ❌ Needs retraining |

---

## 📊 Streamlit Dashboard

**🏠 Home** — Total transactions, fraud count, fraud rate, customers

**📈 Monthly Trends** — Transaction volume + fraud rate (dual Y-axis), debits vs credits, year/month filters

**🔍 Fraud Analysis** — Fraud by flag type, card brand, merchant category, credit score

**👤 Customer Summary** — Spend by gender, fraud by age group, top 10 high-risk customers

### Features:
- 🌙☀️💻 Dark/Light/System theme toggle
- ⚡ 1-hour query cache
- 🚨 Graceful error handling
- 🔄 Dynamic catalog via `DBT_CATALOG` env var
- 🔒 Streamlit Cloud secrets integration

---

## ⏰ Airflow Pipeline

**Schedule:** Daily at 6:00 AM UTC (`0 6 * * *`)

```
source_freshness → convert_seeds → dbt_seed
                                      │
              ┌───────────────────────┤
              ▼           ▼           ▼
        bronze_txns  bronze_users  bronze_cards
              └───────────┬───────────┘
                          ▼
                      test_bronze
                          │
              ┌───────────┤
              ▼           ▼           ▼
        silver_txns  silver_users  silver_cards
              └───────────┬───────────┘
                          ▼
                      test_silver
                          │
              ┌───────────┤
              ▼           ▼           ▼
        gold_fraud  gold_customer  gold_trends
              └───────────┬───────────┘
                          ▼
                      test_gold
                          ▼
                  dbt_docs_generate
```

**Key features:**
- `profiles.yml` mounted as Docker volume — persists across restarts
- Portable paths via `DBT_PROJECT_DIR` and `DBT_PROFILES_DIR` env vars
- `max_active_runs=1` prevents overlapping runs
- `execution_timeout=2h` prevents hanging tasks
- Source freshness check before any transformation

---

## 🔄 CI/CD Pipeline

**GitHub Actions** runs on every push to `main` and every pull request.

### Workflow: `.github/workflows/dbt_ci.yml`

```
Push to main / PR
      │
      ▼
Checkout code
      │
      ▼
Setup Python 3.12 + uv
      │
      ▼
Install dbt-databricks
      │
      ▼
Create dbt profiles (from GitHub Secrets)
      │
      ▼
Truncate train_fraud_labels to 20 rows (CI optimization)
      │
      ▼
dbt deps → dbt debug → dbt compile → dbt test
```

### GitHub Secrets Required:
| Secret | Description |
|--------|-------------|
| `DATABRICKS_HOST` | Workspace hostname |
| `DATABRICKS_HTTP_PATH` | SQL Warehouse path |
| `DATABRICKS_TOKEN` | Personal access token |
| `DBT_CATALOG` | Catalog name |

---

## 🚀 Setup Guide

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Databricks workspace with SQL Warehouse
- Kaggle account

### Step 1 — Clone
```bash
git clone https://github.com/PriyankaMenghare/Banking-Fraud-Analytics
cd Banking-Fraud-Analytics
```

### Step 2 — Install dependencies
```bash
uv venv
source .venv/bin/activate
uv add dbt-databricks streamlit databricks-sql-connector pandas seaborn matplotlib python-dotenv
```

### Step 3 — Configure dbt profiles
Create `~/.dbt/profiles.yml` (outside project — never committed):
```yaml
banking_fraud_analytics:
  outputs:
    dev:
      type: databricks
      catalog: banking_fraud_analytics_dev
      host: your-workspace.cloud.databricks.com
      http_path: /sql/1.0/warehouses/your-warehouse-id
      token: your-databricks-token
      schema: default
      threads: 4
    prod:
      type: databricks
      catalog: banking_fraud_analytics_prod
      host: your-workspace.cloud.databricks.com
      http_path: /sql/1.0/warehouses/your-warehouse-id
      token: your-databricks-token
      schema: default
      threads: 4
  target: dev
```

### Step 4 — Create `.env`
```bash
cd banking_fraud_analytics
cat > .env << 'EOF'
DATABRICKS_HOST=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-databricks-token
DBT_CATALOG=banking_fraud_analytics_dev
DBT_TARGET=dev
EOF
```

### Step 5 — Download & upload dataset
1. Download from [Kaggle](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets)
2. Upload 3 CSV files to `{catalog}.source` in Databricks

### Step 6 — Generate full seed files
```bash
python scripts/convert_json_to_csv.py
```

### Step 7 — Run dbt pipeline
```bash
dbt debug       # verify connection
dbt deps        # install packages
dbt seed        # load lookup tables
dbt run         # run all 9 models
dbt test        # run all 28+ tests
dbt docs generate && dbt docs serve
```

### Step 8 — Run Streamlit
```bash
cd streamlit
streamlit run app.py
```

### Step 9 — Set up Airflow
```bash
cd airflow

# Configure environment
echo "AIRFLOW_UID=$(id -u)" >> .env
echo "DBT_PROJECT_DIR=../banking_fraud_analytics" >> .env
echo "DBT_PROFILES_DIR=~/.dbt/profiles.yml" >> .env

# Start Airflow
docker compose up airflow-init
docker compose up -d

# Open http://localhost:8080 (airflow/airflow)
```

---

## 🔧 Environment Variables

| Variable | Location | Description | Default |
|----------|----------|-------------|---------|
| `DATABRICKS_HOST` | `.env` | Workspace hostname | Required |
| `DATABRICKS_HTTP_PATH` | `.env` | SQL Warehouse path | Required |
| `DATABRICKS_TOKEN` | `.env` | Personal access token | Required |
| `DBT_CATALOG` | `.env` | Databricks catalog | `banking_fraud_analytics_dev` |
| `DBT_TARGET` | `.env` | dbt target | `dev` |
| `AIRFLOW_UID` | `airflow/.env` | Airflow user ID | `50000` |
| `DBT_PROJECT_DIR` | `airflow/.env` | Path to dbt project | `..` |
| `DBT_PROFILES_DIR` | `airflow/.env` | Path to profiles.yml | `~/.dbt/profiles.yml` |

---

## 🐛 Issues & Solutions

### 1. SSL Certificate Verification Failed
**Error:** `SSLCertVerificationError: certificate verify failed`

**Cause:** Corporate proxy/VPN intercepting SSL on Mac.

**Solution:**
```bash
pip install --upgrade certifi
echo 'export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")' >> ~/.zshrc
echo 'export REQUESTS_CA_BUNDLE=$(python3 -c "import certifi; print(certifi.where())")' >> ~/.zshrc
source ~/.zshrc
code .  # Always launch VS Code from terminal
```

---

### 2. dbt Power User Extension Queries Hanging
**Cause:** VS Code extension's Node.js process has same SSL issue.

**Solution:** Always launch VS Code from terminal — extension inherits SSL env vars.

---

### 3. Databricks SQL Warehouse Cold Start (900s timeout)
**Cause:** Serverless warehouse auto-stopped.

**Solution:** Start warehouse manually from Databricks UI. Set auto-stop to 60 mins during development.

---

### 4. dbt `resolve_ref` Error
**Error:** `AttributeError: 'NoneType' object has no attribute 'resolve_ref'`

**Solution:**
```bash
dbt compile  # regenerate manifest.json
# Cmd+Shift+P → "Restart dbt Server" in VS Code
```

---

### 6. Docker Compose Path Not Portable
**Cause:** Hardcoded absolute path only worked on one machine.

**Solution:** Use environment variables:
```yaml
# airflow/.env
DBT_PROJECT_DIR=../banking_fraud_analytics
DBT_PROFILES_DIR=/your/path/.dbt/profiles.yml

# docker-compose.yaml
- ${DBT_PROJECT_DIR:-..}:/opt/airflow/dbt
- ${DBT_PROFILES_DIR}:/home/airflow/.dbt/profiles.yml:ro
```

---

### 7. Airflow OOM Kill (exit code -9)
**Cause:** `train_fraud_labels` (8.9M rows) exceeded Docker memory.

**Solution:**
- Increased Docker Desktop memory to 6GB
- DAG only seeds `mcc_codes` — `train_fraud_labels` already in Databricks

---

### 8. profiles.yml Lost After Container Restart
**Cause:** Container filesystem resets on restart.

**Solution:** Mount as Docker volume:
```yaml
- ${DBT_PROFILES_DIR}:/home/airflow/.dbt/profiles.yml:ro
```

---

### 9. Redis Unhealthy in Docker
**Solution:** Switch to `LocalExecutor` — no Redis needed:
```bash
# airflow/.env
AIRFLOW__CORE__EXECUTOR=LocalExecutor
```

---

### 10. CloudFetch Slow Warning
**Solution:**
```python
sql.connect(..., use_cloud_fetch=False)
```

---

### 11. GitHub Actions — Large Seed File
**Cause:** `train_fraud_labels.csv` has 8.9M rows — too large for CI.

**Solution:** Truncate to 20 rows in CI workflow:
```yaml
- name: Prepare seed files for CI
  run: |
    head -21 seeds/train_fraud_labels.csv > seeds/train_fraud_labels_ci.csv
    mv seeds/train_fraud_labels_ci.csv seeds/train_fraud_labels.csv
```

---

### 12. Streamlit Cloud — Missing Credentials
**Cause:** `.env` file not available on Streamlit Cloud.

**Solution:** Add secrets in Streamlit Cloud dashboard:
- App settings → Secrets → Add `DATABRICKS_HOST`, `DATABRICKS_HTTP_PATH`, `DATABRICKS_TOKEN`, `DBT_CATALOG`

---

## 📈 Project Results

| Metric | Value |
|--------|-------|
| Total Transactions | 13,305,915 |
| Total Customers | 1,219 |
| Total Fraud Transactions | 13,332 |
| Overall Fraud Rate | 0.10% |
| dbt Models | 9 |
| dbt Tests | 28+ passing |
| Pipeline Schedule | Daily 6AM UTC |
| Dashboard Pages | 4 |
| Airflow Tasks | 14 |
| CI/CD | GitHub Actions on every push |

---

## 🔮 Future Improvements

- [ ] **ML-based fraud detection** using Databricks MLflow
- [ ] **dbt snapshots** to track slowly changing dimensions (e.g. credit score history)
- [ ] **Email/Slack alerts** in Airflow on test failures
- [ ] **Great Expectations** for advanced data quality
- [ ] **Production catalog** — separate dev/prod environments

---

## 👩‍💻 Author

**Priyanka Menghare**
- GitHub: [@PriyankaMenghare](https://github.com/PriyankaMenghare)
- Project: [Banking-Fraud-Analytics](https://github.com/PriyankaMenghare/Banking-Fraud-Analytics)
- Dashboard: [Live Demo](https://priyankamenghare-banking-fraud-analytics.streamlit.app)

---

*Built as part of a data engineering learning journey covering Databricks, dbt, Apache Airflow, Streamlit, and GitHub Actions.*
