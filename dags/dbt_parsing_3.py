

from pendulum import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
import logging
from utils.dbt import manifest_parsing

"""
Test connection to hive by running a simple dbt model
Also prints out the airflow home directory

"""

with DAG(
    "dbt_parsing_test_3",
    start_date=datetime(2020, 12, 23),
    description="An Airflow DAG to test connection to hive by running a dbt model",
    schedule_interval=None,
    catchup=False,
    default_args={
    },
) as dag:
    start = DummyOperator(
        task_id="start"
    )

    models = manifest_parsing(model_tag='staged')[:24]

    log_to_dag = PythonOperator(
        task_id="log_to_dag",
        python_callable=lambda: logging.info(f"Models: {models}"),
        dag=dag
    )

    # with TaskGroup(group_id='model_group', dag=dag) as model_group:
    #     for model_id in models:
    #         BashOperator(
    #             task_id=f"dbt_{model_id}",
    #             bash_command=f"cd /opt/airflow/dbt && dbt run --profiles-dir . --select {model_id.split('.')[-1]}",
    #             dag=dag,
    #         )

    model_group_3 = BashOperator(
        task_id="dbt_group_3",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir . --select tag:group_3",
        dag=dag,
    )

    ready = DummyOperator(
        task_id="ready"
    )

    (
        start
        >> log_to_dag
        >> model_group_3
        >> ready
    )
