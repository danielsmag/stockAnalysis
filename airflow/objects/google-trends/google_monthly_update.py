from pytrends.request import TrendReq
import pandas as pd
from typing import List
from pandas import DataFrame
from google_abc import PytrendsABC

class GoogleTrendsModel(PytrendsABC):

    __slots__: List[str] = [
        "pytrends",
        "kw_list"
    ]

    def __init__(self) -> None:
        super().__init__(geo='US')


    def run(self) -> None:
        self.MongoConn.create_conn()
        self.kw_list = self.MongoConn.load_data_to_json(index_value='kw_google_trends',collection='tickers_to_load')

    def load_tickers(self):







