import os
import sys
import json
import boto3
from decimal import Decimal

# environment variables
table_name_m = os.environ.get('TABLE_NAME_MINUTE', 'ap-northeast-1')
table_name_h = os.environ.get('TABLE_NAME_HOUR', 'ap-northeast-1')
table_name_d = os.environ.get('TABLE_NAME_DAY', 'ap-northeast-1')
table_name = table_name_m

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):

    token_dict = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'ltc': 'litecoin',
        'bch': 'bitcoin-cash',
        'ada': 'cardano',
        'bnb': 'binancecoin',
        'dot': 'polkadot',
        'link': 'chainlink'
    }

    try:
        region = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-1')
        dynamodb = boto3.resource ("dynamodb", region_name=region)

        query = event['queryStringParameters']
        print('query: {}'.format(query))
        n = query['n']
        print('name: {}'.format(n))
        p = query['p']
        print('period: {}'.format(p))

        if n in token_dict.keys():
            n = token_dict[n]
        else:
            n = None

        if p == 'm':
            table_name = table_name_m
        elif p == 'h':
            table_name = table_name_h
        elif p == 'd':
            table_name = table_name_d
        else:
            table_name = None

        table = dynamodb.Table(table_name)
        res = table.get_item(Key={'name': n})

        res = res['Item']
        print(res)

        return {
            "statusCode": 200,
            "body": json.dumps(res, default=decimal_default),
            "headers": {
                'content-type': 'application/json'
            },
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": e.args
            }),
            "headers": {
                'content-type': 'application/json'
            },
        }

if __name__ == "__main__":
    lambda_handler(json.loads(sys.args[1]), {})
