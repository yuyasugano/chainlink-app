import os
import sys
import json
import requests
import pandas as pd
from coingecko import CoinGecko
from dynamodb import DynamoDB

# environment variables
table_name = os.environ.get('TABLE_NAME', 'ap-northeast-1')

def price(coin, vs_currency, days):
    obj = CoinGecko()
    df = obj.getCoinData(coin, vs_currency, days)
    return df

def prices(coins, vs_currency, days):
    obj = CoinGecko()
    df = pd.DataFrame()
    for coin in coins:
        d = obj.getCoinData(coin, vs_currency, days)
        df = pd.concat([df, d[['Close']]], axis=1, sort=True, join='outer')
    return df

def append_features(df, window=3):
    df['return'] = df.rename(columns={'Close': 'y'}).loc[:, 'y'].pct_change(window).fillna(method='bfill')
    df['sma'] = df['Close'].rolling(window=window).mean().fillna(method='bfill')
    df['dis'] = df['Close']/df['sma'] # disparity df.describe()
    return df

def put_item(item):
    obj = DynamoDB(table_name)
    ret = obj.ingest_new(item)
    print(item)
    print(ret)

def lambda_handler(event, context):
    if event['operation'] == 'test':
        coin = 'bitcoin'
        feature_names = ['Close', 'return', 'sma', 'dis']
        df = price(coin, 'usd', '1')
        df = append_features(df, 4)
        df = df[feature_names]
        df.dropna(how='any', inplace=True)

        item = {
            'name': coin,
            'Close': df.loc[df.index[-1], 'Close'],
            'return': df.loc[df.index[-1], 'return'],
            'sma': df.loc[df.index[-1], 'sma'],
            'dis': df.loc[df.index[-1], 'dis']
            }

        put_item(item)
    elif event['operation'] == 'test2':
        coins = ['bitcoin', 'ethereum', 'chainlink']
        df = prices(coins, 'usd', '1')
        df.dropna(how='any', inplace=True)
        df.columns = coins
    else:
        raise ValueError('Invalid Operation')

if __name__ == "__main__":
    lambda_handler(json.loads(sys.args[1]), {})
