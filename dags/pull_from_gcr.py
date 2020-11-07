from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.today() - timedelta(weeks=1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG("pull_from_gcr", default_args=default_args, schedule_interval=None) as dag:
    DockerOperator(
        task_id="pull_from_gcr",
        image="asia.gcr.io/cloud-registry-test/python-sample:latest",
        docker_conn_id="gcr_conn",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )
