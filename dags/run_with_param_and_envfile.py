"""
Configuration JSON (Optional)に以下を指定して実行する
{
    "version": "3.10.0a2",
    "args": "-c \"from datetime import datetime; print(datetime.now())\""
}
"""
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta
from dotenv import dotenv_values

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.today() - timedelta(weeks=1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG("run_with_param_and_env", default_args=default_args, schedule_interval=None) as dag:
    DockerOperator.template_fields = tuple(list(DockerOperator.template_fields) + ["image"])  # template対象に`image`を追加
    DockerOperator(
        task_id="run_with_param_and_env",
        image="python:{{ dag_run.conf['version'] }}",  # jinja2でConfiguration JSON設定値埋め込み
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment=dotenv_values(dotenv_path="/usr/local/airflow/envfiles/sample.env"),  # dotenvでファイルからdictにロードして、DockerOperatorに渡す
        volumes=["/Users/rinoguchi/workspace/docker-airflow/credentials/:/credentials/"],  # Dockerエンジンが動いているMacOSのパスを指定
        # command="""python -c "from os import environ; print(environ.get('KEY1')); print(environ.get('KEY2'));" """
        command="python {{ dag_run.conf['args'] }}",  # jinja2でConfiguration JSON設定値埋め込み
    )
