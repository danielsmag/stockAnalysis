from celery import shared_task
from celery.contrib.abortable import AbortableTask
from pandas import DataFrame
from time import sleep
from generalObjects.conn_postgres import ConnPostgres
from generalObjects.googleTrends.google_trends_models import GoogleAnalyzes
import base64,json
import requests
from typing import Dict
from os import environ
from dotenv import load_dotenv
load_dotenv()

credentials: str = base64.b64encode(
    f'{environ.get("_AIRFLOW_WWW_USER_USERNAME")}:{environ.get("_AIRFLOW_WWW_USER_PASSWORD")}').\
        decode('utf-8')
AIRFLOW_URL: str = 'http://130.185.119.199:80'
airflow_terminal_states:list = ["success", "failed", "error"]



@shared_task(bind=True, base=AbortableTask)
def update_db(self,kw):
    connPostgres = ConnPostgres(db='analytics',server='airflow')
    connPostgres.create_conn()
    new_kw_df: DataFrame = DataFrame(data=kw, columns=['kw'])
    if not new_kw_df.empty:
        new_kw_df.to_sql('kw', con=connPostgres.get_engine(), schema='google-trends', if_exists='replace', index=False)
        print(new_kw_df)
    connPostgres.close_conn()
    return 'DONE'

@shared_task(bind=True, base=AbortableTask)
def run_airflow_dag(self,dag_id: str) -> bool:
    assert isinstance(dag_id,str), "dag_id must be string"
    status_to_retuen: bool = False
    # DAG_ID: str = 'update_socgen_new'
    headers:Dict[str,str] = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}'
    }
    trigger_endpoint: str = f"/api/v1/dags/{dag_id}/dagRuns"
    response = requests.post(AIRFLOW_URL + trigger_endpoint, headers=headers, data=json.dumps({}))
    if response.status_code != 200:
        print("Failed to trigger the DAG.")
        exit()
    dag_run_data = response.json()
    dag_run_id = dag_run_data["dag_run_id"]
    status_endpoint = f"/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}"

    while True:
        response: response = requests.get(AIRFLOW_URL + status_endpoint, headers=headers)
        data = response.json()
        state = data["state"]

        print(f"DAG run state: {state}")

        if state.lower() in airflow_terminal_states:
            if state.lower() =='success':
                status_to_retuen = True
            break

        sleep(10)
    print(f"DAG run {dag_run_id} has finished with state: {state}")

    return status_to_retuen
