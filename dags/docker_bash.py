from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 11, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG("docker_bash_sample", default_args=default_args, schedule_interval=timedelta(1)) as dag:
    t1 = BashOperator(task_id="print_start", bash_command="echo $(date '+%Y-%m-%d %H:%M:%S') started.")

    t2 = DockerOperator(
        task_id='docker_command',
        image='centos:latest',
        api_version='auto',
        auto_remove=True,
        command="sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    t3 = BashOperator(task_id="print_finish", bash_command="echo $(date '+%Y-%m-%d %H:%M:%S') finished.")
    t1 >> t2 >> t3
