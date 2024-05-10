import json
from src.Classes.User import DatabaseSyncedProfile
import stripe
import os

stripe.api_key = os.environ['STRIPE_API_KEY']

def handle_stripe_event(event):
    event_data = event['data']['object']
    print(event_data)
    if event_data['object'] == 'payment_intent' and event_data['status'] == 'succeeded':
        user_id = event_data['metadata']['user_id']
        price_id = event_data['metadata']['plan_id']
        
        user = DatabaseSyncedProfile.from_id(user_id)
        
        if "plan_" in price_id:
            user.expiry_date = None
        elif "credits_" in price_id:
            print("Credits integration pending!")
        

# Stub function to handle webhook events from Stripe
def handler(event, context):
    # Process Stripe webhook event
    handle_stripe_event(event)
    
    # Respond to Stripe with success
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Webhook received successfully'})
    }
