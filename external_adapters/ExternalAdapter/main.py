import json

from adapter import Adapter

def lambda_handler(event, context):
    adapter = Adapter(event)
    return adapter.result

