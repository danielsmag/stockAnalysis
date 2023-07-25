from pytrends.request import TrendReq
import pandas as pd
from typing import List

class GoogleTrendsModel:

    __slots__: List[str] = [

    ]

    def __init__(self) -> None:
        self.pytrends = TrendReq(hl='en-US')


    def run(self):
        pass

    def query(self,kw_list: list,timestamp: str ):
        assert isinstance(kw_list,list), "kw_list must be list"
        assert isinstance(timestamp,str), "timstamp must be str"
        self.pytrends.build_payload(kw_list, cat=0, timeframe=timestamp, geo='US', gprop='')
        temp_df = self.pytrends.interest_over_time()












# Create a pytrends object
pytrends = TrendReq(hl='en-US', tz=360)

# Define the search keywords
kw_list = ['Blockchain']

# Build the payload
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

# Request the interest over time
interest_over_time_df = pytrends.interest_over_time()

print(interest_over_time_df)
