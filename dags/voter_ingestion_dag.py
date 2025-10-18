from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/scripts')  # so Airflow can import your script

from ingest_voter_data import ingest_voter_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='voter_data_ingestion',
    default_args=default_args,
    start_date=datetime(2025, 10, 18),
    schedule_interval='@daily',  # or None for manual
    catchup=False,
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_voter_data',
        python_callable=ingest_voter_data
    )
