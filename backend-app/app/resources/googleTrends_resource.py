from celery import shared_task
from celery.contrib.abortable import AbortableTask
from flask_restful import Resource,reqparse
from flask import Blueprint,request
from generalObjects.conn_postgres import ConnPostgres
from typing import List
from pandas import read_sql_query, DataFrame
from app.models.googleTrends_model import kwSchema,PostKwSchema,UpdateData
from time import sleep
from app.tasks.task import update_db
# from app.objects.googleTtrends.google_trends_models import GoogleAnalyzes
from generalObjects.googleTrends.google_trends_models import GoogleAnalyzes
from app.tasks.task import update_all_google_trends,run_airflow_dag


kw_schema = kwSchema()
PostKwSchema = PostKwSchema()

class KW_list(Resource):
    __slots__: List[str] = [
        "connPostgres"
    ]

    def __init__(self) -> None:
        print('KW_list init')
        self.connPostgres = ConnPostgres(db='analytics',server='airflow')

    def get(self):
        self.connPostgres.create_conn()
        query = 'SELECT * FROM "google-trends"."kw"'
        df: DataFrame = read_sql_query(query, self.connPostgres.get_engine())
        df_dict = df.to_dict(orient='list')
        print('df of kw',df_dict)
        self.connPostgres.close_conn()
        return kw_schema.dump({"kw": df_dict['kw']}),200

    def post(self):
        self.connPostgres.create_conn()
        args = PostKwSchema.load(request.get_json())
        kw = args.get('kw')
        task = update_db.delay(kw)
        new_kw_df: DataFrame = DataFrame(data=args.get('kw'), columns=['kw'])

        # if not new_kw_df.empty:
        #     new_kw_df.to_sql('kw', con=self.connPostgres.get_engine(), schema='google-trends', if_exists='replace', index=False)
        #     print(new_kw_df)
        # self.connPostgres.close_conn()
        return {"message": "Data updated successfully"}, 200

class UpdateData(Resource):
    __slots__:List[str] = [

    ]

    def __init__(self) -> None:
        pass

    def post(self)-> tuple:
        reslut_dict: dict = {}
        args: dict = UpdateData.load(request.get_json())
        timeframe = args.get('timeframe')
        for timef in timeframe:
            dag_name: str = f"Google_Trends_{timef}"
            print(f'run dag {dag_name}')
            status:bool = run_airflow_dag(dag_id=dag_name)
            reslut_dict[dag_name] = status

        return reslut_dict, 200

