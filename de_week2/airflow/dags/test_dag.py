import os
import logging
from datetime import datetime

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq


default_args = {
    "owner": "airflow",
    "start_date": datetime(2022,1,1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="test_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=True,
    max_active_runs=2,
    tags=['dtc-de'],
    ) as dag:

    bash_task = BashOperator(
    task_id="execution_date",
    bash_command="echo 'execution date : {{ ds }} ds_add: {{ macros.ds_add(ds, 2) }}'"
    )
