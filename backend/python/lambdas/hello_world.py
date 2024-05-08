import json
import wikipedia
from src.random_drink import random_drink

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello World! Here is a random drink: ' + random_drink(),
            'dune_2_summary':"Nothing, just import of wikipedia to see if packages work" 
        })
    }
