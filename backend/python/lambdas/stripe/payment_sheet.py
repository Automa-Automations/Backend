import json

def handler(event, context):
    userId = event['userId']
    priceId = event['planId']
    # Check supabase for customer

