import json

def handler(event, context):
    userId = event['userId']
    priceId = event['planId']

    # Get User from userId

