from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

DBT_PROJECT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = "/home/airflow/.dbt"
DBT_BIN = "/home/airflow/.local/bin/dbt"
DBT_TARGET = os.getenv("DBT_TARGET", "dev")

def dbt_task(task_id, command, retries=1):
    return BashOperator(
        task_id=task_id,
        bash_command=f'cd {DBT_PROJECT_DIR} && {DBT_BIN} {command} --profiles-dir {DBT_PROFILES_DIR} --target {DBT_TARGET}',
        retries=retries,
        retry_delay=timedelta(minutes=2),
    )

default_args = {
    'owner': 'priyanka',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
    'execution_timeout': timedelta(hours=2),
}

with DAG(
    dag_id='banking_fraud_analytics',
    default_args=default_args,
    description='Daily dbt pipeline for banking fraud analytics',
    schedule='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['banking', 'dbt', 'fraud'],
) as dag:

    # Source freshness check
    source_freshness = dbt_task(
        'dbt_source_freshness',
        'source freshness'
    )
    convert_seeds = BashOperator(
        task_id='convert_seeds',
        bash_command=f'cd {DBT_PROJECT_DIR} && python scripts/convert_json_to_csv.py',
    )

    # Seeds — only reload small lookup table
    seed = dbt_task('dbt_seed', 'seed --select mcc_codes')

    # Bronze — parallel
    bronze_transactions = dbt_task('bronze_transactions', 'run --select bronze_transactions')
    bronze_users = dbt_task('bronze_users', 'run --select bronze_users')
    bronze_cards = dbt_task('bronze_cards', 'run --select bronze_cards')

    # Bronze tests
    test_bronze = dbt_task('test_bronze', 'test --select bronze')

    # Silver — parallel
    silver_transactions = dbt_task('silver_transactions', 'run --select silver_transactions')
    silver_users = dbt_task('silver_users', 'run --select silver_users')
    silver_cards = dbt_task('silver_cards', 'run --select silver_cards')

    # Silver tests
    test_silver = dbt_task('test_silver', 'test --select silver')

    # Gold — parallel
    gold_fraud = dbt_task('gold_fraud_analysis', 'run --select gold_fraud_analysis')
    gold_customer = dbt_task('gold_customer_summary', 'run --select gold_customer_summary')
    gold_trends = dbt_task('gold_monthly_trends', 'run --select gold_monthly_trends')

    # Gold tests
    test_gold = dbt_task('test_gold', 'test --select gold')

    # Docs
    docs = dbt_task('dbt_docs_generate', 'docs generate')

    # Dependencies
    source_freshness >> convert_seeds >> seed >> [bronze_transactions, bronze_users, bronze_cards]
    [bronze_transactions, bronze_users, bronze_cards] >> test_bronze
    bronze_transactions >> silver_transactions
    bronze_users >> silver_users
    bronze_cards >> silver_cards
    [silver_transactions, silver_users, silver_cards] >> test_silver
    silver_transactions >> [gold_fraud, gold_trends]
    [silver_transactions, silver_users] >> gold_customer
    [gold_fraud, gold_customer, gold_trends] >> test_gold
    test_gold >> docs