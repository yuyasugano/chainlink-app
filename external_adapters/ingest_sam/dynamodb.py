import os
import json
import boto3
import decimal

region = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-1')
dynamodb = boto3.resource('dynamodb', region_name=region)

class DynamoDB(object):

    def __init__(self, table_name):
        self.table_name = table_name

    def ingest_new(self, item):
        try:
            print('table_name: {}'.format(self.table_name))
            item = json.dumps(item)
            item = json.loads(item, parse_float=decimal.Decimal)
            current_table = dynamodb.Table(self.table_name)
            response = current_table.put_item(Item = item)
            return 'put_item succeeded {}'.format(response)
        except Exception as e:
            return 'put_item failed {}'.format(e.args)
