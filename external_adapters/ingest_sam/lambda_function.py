import os
import sys
import json
import requests
import pandas as pd
from coingecko import CoinGecko
from dynamodb import DynamoDB

# environment variables
table_name_m = os.environ.get('TABLE_NAME_MINUTE', 'ap-northeast-1')
table_name_h = os.environ.get('TABLE_NAME_HOUR', 'ap-northeast-1')
table_name_d = os.environ.get('TABLE_NAME_DAY', 'ap-northeast-1')
table_hash = {'m': table_name_m, 'h': table_name_h, 'd': table_name_d}

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

def moving_average(df, n):
    """ Calculate the moving average for the given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['Close'].rolling(n, min_periods=n).mean(), name='sma')
    df = df.join(MA)
    return df

def append_features(df, window=3):
    df['return'] = df['Close'].pct_change(window)
    df['sma'] = df['Close'].rolling(window=window).mean()
    df['disparity'] = df['Close']/df['sma'] # disparity df.describe()
    df['ema'] = df['Close'].ewm(span=window, min_periods=window).mean()
    df['momentum'] = df['Close'].diff(window)
    df['std'] = df['Close'].rolling(window, min_periods=window).std()
    df.fillna(method='bfill')
    return df

def put_item(table_name, item):
    obj = DynamoDB(table_name)
    ret = obj.ingest_new(item)
    print(ret)

def lambda_handler(event, context):
    tokens = ['bitcoin', 'ethereum', 'litecoin', 'bitcoin-cash', 'cardano', 'binancecoin', 'polkadot', 'chainlink']

    if event['operation'] == 'show':
        tokens = ['bitcoin', 'ethereum']
        df = prices(tokens, 'usd', '180')
        df.columns = tokens
        df.dropna(how='any', inplace=True)
        print(df)

    elif event['operation'] == 'ingest_m':
        vs_currency = 'usd'
        days = ['1']
        windows = [3, 5, 20]
        feature_names = ['return', 'sma', 'disparity']
        for t in tokens:
            for i, day in enumerate(days):
                r = {}
                s = {}
                d = {}
                e = {}
                m = {}
                std = {}
                for w in windows:
                    df = price(t, vs_currency, day)
                    df = append_features(df, w)
                    df.dropna(how='any', inplace=True)

                    r[w] = df.loc[df.index[-1], 'return']
                    s[w] = df.loc[df.index[-1], 'sma']
                    d[w] = df.loc[df.index[-1], 'disparity']
                    e[w] = df.loc[df.index[-1], 'ema']
                    m[w] = df.loc[df.index[-1], 'momentum']
                    std[w] = df.loc[df.index[-1], 'std']
                    
                item = {
                    'name': t,
                    'return': r,
                    'sma': s,
                    'disparity': d,
                    'ema': e,
                    'momentum': m,
                    'std': std
                }
                print('Token={} day={} item={}'.format(t, day, item))
                put_item(table_hash['m'], item)
    elif event['operation'] == 'ingest_h':
        vs_currency = 'usd'
        days = ['7']
        windows = [3, 5, 20]
        feature_names = ['return', 'sma', 'disparity']
        for t in tokens:
            for i, day in enumerate(days):
                r = {}
                s = {}
                d = {}
                e = {}
                m = {}
                std = {}
                for w in windows:
                    df = price(t, vs_currency, day)
                    df = append_features(df, w)
                    df.dropna(how='any', inplace=True)

                    r[w] = df.loc[df.index[-1], 'return']
                    s[w] = df.loc[df.index[-1], 'sma']
                    d[w] = df.loc[df.index[-1], 'disparity']
                    e[w] = df.loc[df.index[-1], 'ema']
                    m[w] = df.loc[df.index[-1], 'momentum']
                    std[w] = df.loc[df.index[-1], 'std']
                    
                item = {
                    'name': t,
                    'return': r,
                    'sma': s,
                    'disparity': d,
                    'ema': e,
                    'momentum': m,
                    'std': std
                }
                print('Token={} day={} item={}'.format(t, day, item))
                put_item(table_hash['h'], item)
    elif event['operation'] == 'ingest_d':
        vs_currency = 'usd'
        days = ['180']
        windows = [3, 5, 20]
        feature_names = ['return', 'sma', 'disparity']
        for t in tokens:
            for i, day in enumerate(days):
                r = {}
                s = {}
                d = {}
                e = {}
                m = {}
                std = {}
                for w in windows:
                    df = price(t, vs_currency, day)
                    df = append_features(df, w)
                    df.dropna(how='any', inplace=True)

                    r[w] = df.loc[df.index[-1], 'return']
                    s[w] = df.loc[df.index[-1], 'sma']
                    d[w] = df.loc[df.index[-1], 'disparity']
                    e[w] = df.loc[df.index[-1], 'ema']
                    m[w] = df.loc[df.index[-1], 'momentum']
                    std[w] = df.loc[df.index[-1], 'std']

                item = {
                    'name': t,
                    'return': r,
                    'sma': s,
                    'disparity': d,
                    'ema': e,
                    'momentum': m,
                    'std': std
                }
                print('Token={} day={} item={}'.format(t, day, item))
                put_item(table_hash['d'], item)
    else:
        raise ValueError('Invalid Operation')

if __name__ == "__main__":
    lambda_handler(json.loads(sys.args[1]), {})
