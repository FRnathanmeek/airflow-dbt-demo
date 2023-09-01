

from pendulum import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator


"""
Test connection to hive by running a simple dbt model
Also prints out the airflow home directory

"""

with DAG(
    "dbt_basic_dag",
    start_date=datetime(2020, 12, 23),
    description="A sample Airflow DAG to invoke dbt runs using a BashOperator",
    schedule_interval=None,
    catchup=False,
    default_args={
    },
) as dag:
    start = DummyOperator(
        task_id="start"
    )

    dbt_run_abom_edges_staged = BashOperator(
        task_id="dbt_run_abom_edges_staged",
        bash_command="cd ${AIRFLOW_HOME}/dbt && dbt run --profiles-dir . --select abom_edges_staged",
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
        >> dbt_run_abom_edges_staged
        >> dbt_echo_home
        >> ready
    )
