from abc import ABC ,abstractmethod
from typing import List
from pytrends.request import TrendReq

class PytrendsABC:

    __slots__: List[str] = [
        "pytrends"
    ]

    def __init__(self):
        self.pytrends = TrendReq(hl='en-US')

    def get_tickers(self):
        pass

    def build_payload(self,kw_list: list, timestemp:str) -> None:
        self.pytrends.build_payload(kw_list, cat=0, timeframe=timestemp, geo='US', gprop='')

    def interest_over_time(self):
        pass