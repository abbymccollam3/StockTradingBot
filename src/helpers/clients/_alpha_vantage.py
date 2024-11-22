import pytz
import requests

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from urllib.parse import urlencode
from decimal import Decimal
from decouple import config

def transform_alpha_vantage_result(timestamp_str, result_val):
    # unix_timestamp = result.get('t') / 1000
    # utc_timestamp = datetime.fromtimestamp(unix_timestamp, tz=pytz.timezone('UTC'))
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    eastern = pytz.timezone("US/Eastern")
    utc = pytz.utc
    timestamp = eastern.localize(datetime.strptime(timestamp_str, timestamp_format)).astimezone(utc)
    return {
     'open_price': Decimal(result_val['1. open']),
     'close_price': Decimal(result_val['4. close']),
     'high_price': Decimal(result_val['2. high']),
     'low_price': Decimal(result_val['3. low']),
     'volume': int(result_val['5. volume']),
     'time': timestamp,
    }

ALPHA_VANTAGE_API_KEY = config("ALPHA_VANTAGE_API_KEY", default=None, cast=str) 

@dataclass
class AlphaVantageAPIClient: #API parameters
    ticker: str = "AAPL"
    function: Literal["TIME_SERIES_INTRADAY"] = "TIME_SERIES_INTRADAY"
    interval: Literal["1min", "5min", "15min", "30min", "60min"] = "1min"
    api_key: str = ""
    
    def get_api_key(self):
        return self.api_key or ALPHA_VANTAGE_API_KEY

    # don't want to expose API key, so pass in headers instead
    def get_headers(self):
        api_key = self.get_api_key()
        return {
            "Authorization": f"Bearer {api_key}"
        }

    def get_params(self):
        return {
            "apikey" : self.get_api_key,
            "symbol" : self.ticker,
            "interval" : self.interval,
            "function" : self.function,
        }

    def generate_url(self, pass_auth=False):
        path = "/query"
        url = f"https://www.alphavantage.co{path}"
        params = self.get_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}" # appends base url with encoded params
        if pass_auth:
            api_key = self.get_api_key()
            url += "&api_key={api_key}"
        return url

    # fetching the raw data
    def perform_request(self):
        headers = self.get_headers()
        url = self.generate_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status() # not successful -> raises errors
        return response.json()

    
    def get_stock_data(self):
        data = self.perform_request() # making GET request to Polygon API
        dataset_key = [x for x in list(data.keys()) if not x.lower() == "meta data"][0]
        results = data[dataset_key]
        dataset = []
        for timestamp_str in results.keys():
            dataset.append(
                transform_alpha_vantage_result(timestamp_str, results.get(timestamp_str))
            )
        return dataset
        