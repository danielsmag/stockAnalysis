from pandas import DataFrame, read_sql_query,concat
from typing import List,Dict
from pytrends.request import TrendReq
import time, asyncio
from typing import List
from concurrent.futures import ThreadPoolExecutor
from generalObjects.conn_postgres import ConnPostgres
from generalObjects.utils.utils import GoogleTrendsResultDictModel
from pydentic import validate_arguments

class GoogleAnalyzes:

    __slots__: List[str] = [
        "kw_add",
        "geo",
        "kw_list",
        "pytrends",
        "connPostgres"
    ]

    def __init__(self, kw_add=[]):
        self._initialize_objects()
        self.kw_add = kw_add
        self.geo = 'US'
        self.kw_list: List[str] = []
        self.kw_list.extend(self.load_kw())

    def _initialize_objects(self):
        self.pytrends = TrendReq(hl='en-US')
        self.connPostgres = ConnPostgres(db='analytics',server='AIRFLOW')

    def load_kw(self):
        self.connPostgres.create_conn()
        query = 'SELECT * FROM "google-trends".kw'
        df: DataFrame = read_sql_query(query, self.connPostgres.get_engine())
        kw_list = df['kw'].drop_duplicates().tolist()
        self.connPostgres.close_conn()
        if self.kw_add:
            kw_list.append(self.kw_add)
        kw_list = list(set(kw_list))
        return kw_list

    async def _fetch_data(self, method, timeframe):
        loop = asyncio.get_running_loop()
        self.pytrends.build_payload(self.kw_list, cat=0, timeframe=timeframe, geo=self.geo, gprop='')

        def fetch():
            print(method)
            time.sleep(1)
            return method()

        return await loop.run_in_executor(None, fetch)

    async def _get_data(self,timeframe):
        assert isinstance(timeframe,str)
        print('kw_list', self.kw_list)
        task1 = self._fetch_data(method=self.pytrends.related_queries, timeframe=timeframe)
        task2 = self._fetch_data(method=self.pytrends.related_topics, timeframe=timeframe)
        return await asyncio.gather(task1, task2)

    def past_7_days(self)-> bool:
        try:
            self._load_data(timeframe='now 7-d')
        except Exception as e:
            print(e)
            return False
        return True

    def past_30_days(self) -> bool:
        try:
            self._load_data(timeframe='today 1-m')
        except Exception as e:
            print(e)
            return False
        return True

    def past_3_month(self) -> bool:
        try:
            self._load_data(timeframe='today 3-m')
        except Exception as e:
            print(e)
            return False
        return True

    def _load_data(self,timeframe: str):
        base_dataframe: DataFrame = DataFrame(columns=['kw','query','value'])
        reslut_dict: dict = {'related_queries':{'top':base_dataframe.copy(deep=True),
                                                'rising':base_dataframe.copy(deep=True)},
                             'related_topics':{'top':base_dataframe.copy(deep=True),
                                               'rising':base_dataframe.copy(deep=True)}}
        related_queries_dict,related_topics_dict = asyncio.run(self._get_data(timeframe=timeframe))
        reslut_dict = self._process_result(result_dict=reslut_dict,
                                           result_process_dict=related_queries_dict,
                                           query_name='related_queries')
        reslut_dict = self._process_result(result_dict=reslut_dict,
                                           result_process_dict=related_topics_dict,
                                           query_name='related_topics')

        for relates, value in reslut_dict.items():
            for kind, v in reslut_dict[relates]:
                df_name: str = f'{relates}_{kind}'
                df = v
                if isinstance(df,DataFrame) and not df.empty:
                    df.to_sql(name=df_name, con=self.connPostgres.get_engine(),if_exists='replace',schema='google-trends')

    @validate_arguments
    def _process_result(self, result_dict: dict, result_process_dict:dict,query_name:str) -> dict:
        for kw,val in result_process_dict.items():
            if isinstance(val['top'],DataFrame):
                df:DataFrame = val['top']
                df = df[['query','value']]
                df['kw'] = kw
                result_dict[query_name]['top'] = concat([result_dict[query_name]['top'],df])
            if isinstance(val['rising'],DataFrame):
                df:DataFrame = val['rising']
                df = df[['query','value']]
                df['kw'] = kw
                result_dict[query_name]['rising'] = concat([result_dict[query_name]['rising'],df])
        return result_dict
