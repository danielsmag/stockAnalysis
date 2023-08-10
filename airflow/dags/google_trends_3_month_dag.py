from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
from typing import List,Union,Dict
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from generalObjects.googleTrends.google_trends_models import GoogleAnalyzes


class GooogleTrendsMonthly:

    __slots__:List[str] = [
        "dag_id",
        "other_dag_id",
        "other_task_id",
        "default_args",
        "dag",
        "conf_dict",
        "SodSummery",
        "to_email",

    ]

    def __init__(self, conf_dict: dict = {} ) -> None:
        self._initialize_objects()
        self.conf_dict: dict = conf_dict
        self.dag_id: str = 'Google_Trends_past_3_month'
        self.default_args: dict = {
            'owner': 'airflow',
            'depends_on_past': False,
            'start_date': datetime(2023, 5, 10),
            'email_on_failure': True,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
        }
        self.dag:DAG = self.create_dag()

    def _initialize_objects(self):
        self.GoogleAnalyzes: GoogleAnalyzes = GoogleAnalyzes()

    def create_dag(self)-> DAG:
        tasks_3m_days: list = []

        dag: DAG = DAG(
            dag_id=self.dag_id,
            default_args=self.default_args,
            schedule_interval=None,
            description='update google trends 3 momth ',
            max_active_runs = 1,
            catchup=False)

        update_monthly: PythonOperator = PythonOperator(
            task_id='update_monthly',
            python_callable=self.GoogleAnalyzes.past_3m_days,
            op_args=[],
            provide_context=True,
            dag=dag
        )
        tasks_3m_days.append(update_monthly)

        for i in range(len(tasks_3m_days) - 1):
            tasks_3m_days[i] >> tasks_3m_days[i + 1]
        return dag

    def get_dag(self)-> DAG:
        return self.dag


dag_creator = GooogleTrendsMonthly()
dag_socgen = dag_creator.get_dag()
