import os
import sys
import json
import boto3
from decimal import Decimal

# environment variables
table_name = os.environ.get('TABLE_NAME', 'ap-northeast-1')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):

    try:
        region = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-1')
        dynamodb = boto3.resource ("dynamodb", region_name=region)

        query = event['queryStringParameters']
        print('query: {}'.format(query))
        key = query['key']
        print('key: {}'.format(key))

        print('table_name: {}'.format(table_name))
        table = dynamodb.Table(table_name)
        res = table.get_item(Key={'name': 'bitcoin'})
        # value = json.dumps(Decimal(res['Item'][att]), use_decimal=True)

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
