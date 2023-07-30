from flask_restful import Resource
from flask import Blueprint
from generalObjects.conn_postgres import ConnPostgres
from typing import List
from pandas import read_sql_query, DataFrame
from app.models.googleTrends_model import kwSchema
kw_schema = kwSchema()


class KW_list(Resource):
    __slots__: List[str] = [
        "connPostgres"
    ]

    def __init__(self):
        print('KW_list init')
        self.connPostgres = ConnPostgres(db='analytics',server='airflow')
        self.connPostgres.create_conn()

    def get(self):
        query = 'SELECT * FROM "google-trends"."kw"'
        df: DataFrame = read_sql_query(query, self.connPostgres.get_engine())
        df_dict = df.to_dict(orient='list')
        print('df of kw',df_dict)
        return kw_schema.dump({"kw": df_dict['kw']}),200




