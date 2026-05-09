from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'priyanka',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

DBT_PROJECT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = "/home/airflow/.dbt"
DBT_BIN = "/home/airflow/.local/bin/dbt"

def dbt_task(task_id, command):
    return BashOperator(
        task_id=task_id,
        bash_command=f'cd {DBT_PROJECT_DIR} && {DBT_BIN} {command} --profiles-dir {DBT_PROFILES_DIR}',
    )

with DAG(
    dag_id='banking_fraud_analytics',
    default_args=default_args,
    description='Daily dbt pipeline for banking fraud analytics',
    schedule='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['banking', 'dbt', 'fraud'],
) as dag:

    # Seeds
    seed = dbt_task('dbt_seed', 'seed --select mcc_codes')

    # Bronze
    bronze_transactions = dbt_task('bronze_transactions', 'run --select bronze_transactions')
    bronze_users = dbt_task('bronze_users', 'run --select bronze_users')
    bronze_cards = dbt_task('bronze_cards', 'run --select bronze_cards')

    # Silver
    silver_transactions = dbt_task('silver_transactions', 'run --select silver_transactions')
    silver_users = dbt_task('silver_users', 'run --select silver_users')
    silver_cards = dbt_task('silver_cards', 'run --select silver_cards')

    # Gold
    gold_fraud = dbt_task('gold_fraud_analysis', 'run --select gold_fraud_analysis')
    gold_customer = dbt_task('gold_customer_summary', 'run --select gold_customer_summary')
    gold_trends = dbt_task('gold_monthly_trends', 'run --select gold_monthly_trends')

    # Tests per layer
    test_bronze = dbt_task('test_bronze', 'test --select bronze')
    test_silver = dbt_task('test_silver', 'test --select silver')
    test_gold = dbt_task('test_gold', 'test --select gold')

    # Docs
    docs = dbt_task('dbt_docs_generate', 'docs generate')

    # Dependencies
    seed >> [bronze_transactions, bronze_users, bronze_cards]

    bronze_transactions >> silver_transactions
    bronze_users >> silver_users
    bronze_cards >> silver_cards

    [bronze_transactions, bronze_users, bronze_cards] >> test_bronze

    silver_transactions >> gold_fraud
    silver_transactions >> gold_trends
    [silver_transactions, silver_users] >> gold_customer

    [silver_transactions, silver_users, silver_cards] >> test_silver

    [gold_fraud, gold_customer, gold_trends] >> test_gold

    test_gold >> docs