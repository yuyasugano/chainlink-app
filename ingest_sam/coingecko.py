import json
import datetime
import requests
import numpy as np
import pandas as pd

headers = {'Content-Type': 'application/json'}
api_url_base = 'https://api.coingecko.com/api/v3/coins/'
vs_currency = 'usd'
days = '7'

class CoinGecko(object):

    def getCoinData(self, ids, vs, days):
        api_url = '{0}/{1}/ohlc?vs_currency={2}&days={3}'.format(api_url_base, ids, vs, days)
        res = requests.get(api_url, headers=headers)

        if res.status_code == 200:
            df = pd.read_json(res.content.decode('utf-8'))
            df.columns = ['timestamp', 'Open', 'High', 'Low', 'Close']
            df['timestamp'] = df['timestamp']/1000
            df['timestamp'] = df['timestamp'].astype(int)
            df['timestamp'] = df['timestamp'].map(datetime.datetime.utcfromtimestamp)
            df.index = df['timestamp']
            feature_names = ['Open', 'High', 'Low', 'Close']
            df = df[feature_names]
            df.interpolate(limit_direction='both', inplace=True)
            return df
        else:
            return None

