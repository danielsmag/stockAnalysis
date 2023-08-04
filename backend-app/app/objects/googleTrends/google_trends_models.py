from pandas import DataFrame, read_sql_query
from typing import List,Dict
from pytrends.request import TrendReq
import time, asyncio
from typing import List
from concurrent.futures import ThreadPoolExecutor
from generalObjects.conn_postgres import ConnPostgres


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

    def past_7_days(self):
        return asyncio.run(self._get_data(timeframe='now 7-d'))

    def past_30_days(self):
        return asyncio.run(self._get_data(timeframe='today 1-m'))

    def past_3m_days(self):
        return asyncio.run(self._get_data(timeframe='today 3-m'))