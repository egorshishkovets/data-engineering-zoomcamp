import os
import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020,1,20),
    'depends_on_past': False,
}


with DAG(
    'mydag_new_8',
    default_args=default_args,
    schedule_interval='@daily',
    max_active_runs=2,
    catchup=True
) as dag:

    t1 = BashOperator(
        task_id='echo_hi',
        bash_command='echo "Hello"',
    )

    t2 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    dataset_file = "yellow_tripdata_{{ execution_date.strftime(\"%Y-%m\")}}.csv"
    dataset_url = f"https://s3.amazonaws.com/nyc-tlc/trip+data/{dataset_file}"

    t3 = BashOperator(
        task_id = 'custom_date',
        bash_command=f"echo '{dataset_url}'"
        #bash_command=f"curl -sS {dataset_url} > {path_to_local_home}/{dataset_file}",
    )

    t1 >> t2 >> t3