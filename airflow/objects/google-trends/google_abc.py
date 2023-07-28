from abc import ABC ,abstractmethod
from typing import List
from pytrends.request import TrendReq
from pandas import DataFrame
from generalObjects.conn_mongo import MongoConnection


class PytrendsABC:

    __slots__: List[str] = [
        "pytrends",
        "geo",
        "MongoConn"
    ]

    def __init__(self,geo='US') -> None:
        assert isinstance(geo,str)
        self.geo: str= geo
        self.pytrends = TrendReq(hl='en-US')

    def _initialize_objects(self) -> None:
        self.MongoConn = MongoConnection(server='stock', db='stock')


    def build_payload(self,kw_list: list, timestemp:str) -> None:
        assert isinstance(kw_list,list), "kw_list must be list"
        assert isinstance(timestemp,str), "timstamp must be str"
        self.pytrends.build_payload(kw_list, cat=0, timeframe=timestemp, geo=self.geo, gprop='')

    def interest_over_time(self) -> DataFrame:
        result = DataFrame()
        temp_df: DataFrame = self.pytrends.interest_over_time()
        if isinstance(temp_df,DataFrame) and not temp_df.empty:
           result: DataFrame = temp_df
        return result

    def related_topics(self) -> DataFrame:
        result = DataFrame()
        temp_df: DataFrame = self.pytrends.related_topics()
        if isinstance(temp_df,DataFrame) and not temp_df.empty:
           result: DataFrame = temp_df
        return result

    def related_queries(self) -> DataFrame:
        result = DataFrame()
        temp_df = self.pytrends.related_queries()
        if isinstance(temp_df,DataFrame) and not temp_df.empty:
           result: DataFrame = temp_df
        return result

