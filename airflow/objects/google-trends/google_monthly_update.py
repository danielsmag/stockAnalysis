from pytrends.request import TrendReq
import pandas as pd
from typing import List
from pandas import DataFrame

class GoogleTrendsModel:

    __slots__: List[str] = [
        "pytrends"
    ]

    def __init__(self) -> None:
        self.pytrends = TrendReq(hl='en-US')


    def run(self) -> None:
        pass

    def get_ticker(self) -> None:
        pass

    def build_payload(self,kw_list: list, timestemp:str) -> None:
        assert isinstance(kw_list,list), "kw_list must be list"
        assert isinstance(timestemp,str), "timstamp must be str"
        self.pytrends.build_payload(kw_list, cat=0, timeframe=timestemp, geo='US', gprop='')

    def interest_over_time(self) -> DataFrame:
        result = DataFrame()
        temp_df = self.pytrends.interest_over_time()
        if not temp_df.empty():
           result = temp_df
        return result

    def query(self,kw_list: list,timestamp: str ) -> None:
        self.pytrends.build_payload(kw_list, cat=0, timeframe=timestamp, geo='US', gprop='')
        temp_df = self.pytrends.interest_over_time()
        related_topics = pytrends.related_topics()



