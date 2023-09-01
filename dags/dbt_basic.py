"""
A basic dbt DAG that shows how to run dbt commands via the BashOperator

Follows the standard dbt seed, run, and test pattern.
"""

from pendulum import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import logging

# We're hardcoding this value here for the purpose of the demo, but in a production environment this
# would probably come from a config file and/or environment variables!
DBT_PROJECT_DIR = "/opt/airflow/dbt/"


def list_available_files():
    import os
    for path, subdirs, files in os.walk('.'):
        for name in files:
            print(os.path.join(path, name))


with DAG(
    "dbt_basic_dag",
    start_date=datetime(2020, 12, 23),
    description="A sample Airflow DAG to invoke dbt runs using a BashOperator",
    schedule_interval=None,
    catchup=False,
    default_args={
        # "env": {
        #     "DBT_USER": "{{ conn.postgres.login }}",
        #     "DBT_ENV_SECRET_PASSWORD": "{{ conn.postgres.password }}",
        #     "DBT_HOST": "{{ conn.postgres.host }}",
        #     "DBT_SCHEMA": "{{ conn.postgres.schema }}",
        #     "DBT_PORT": "{{ conn.postgres.port }}",
        # }
    },
) as dag:
    start = DummyOperator(
        task_id="start"
    )

    # list_files = PythonOperator(
    #     task_id="list_files",
    #     python_callable=list_available_files,
    # )

    dbt_run_issues_staged = BashOperator(
        task_id="dbt_run_issues_staged",
        bash_command="cd ${AIRFLOW_HOME}/dbt && dbt run --profiles-dir . --select issues_staged",
    )

    dbt_run_abom_edges_staged = BashOperator(
        task_id="dbt_run_abom_edges_staged",
        bash_command="cd ${AIRFLOW_HOME}/dbt && dbt run --profiles-dir . --select abom_edges_staged",
    )

    dbt_run_parts_staged = BashOperator(
        task_id="dbt_run_parts_staged",
        bash_command="cd ${AIRFLOW_HOME}/dbt && dbt run --profiles-dir . --select parts_staged",
    )

    dbt_echo_home = BashOperator(
        task_id="dbt_echo_home",
        bash_command="echo $AIRFLOW_HOME",
    )

    ready = DummyOperator(
        task_id="ready"
    )

    (
        start
        >> [dbt_run_issues_staged, dbt_run_abom_edges_staged, dbt_run_parts_staged]
        >> dbt_echo_home
        >> ready
    )
