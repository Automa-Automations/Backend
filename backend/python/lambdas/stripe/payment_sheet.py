import json 
from src.Classes.User import DatabaseSyncedProfile
import stripe
import traceback
from typing import Optional
import os

stripe.api_key = os.environ['STRIPE_API_KEY']
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']

# TODO: Fetch this from the database
prices = {
    'plan_premium': 2999,
    'plan_exclusive': 5999,
    'plan_standard': 1499
}

def handler(event, context):
    # Extract data from the event
    print(event)
    user_id = event['userId']
    price_id = event['planId']
    
    # Retrieve or create a Stripe customer
    user = DatabaseSyncedProfile.from_id(user_id)
    customer: Optional[stripe.Customer] = None
    if user and user.stripe_customer_id:
        try:
            customer = stripe.Customer.retrieve(user.stripe_customer_id)
        except stripe.StripeError as e:
            print("Failed to retrieve customer", e, traceback.format_exc(), user.stripe_customer_id)
            customer = None

    if not customer:
        customer = stripe.Customer.create()
        user.stripe_customer_id = customer.id
    
    # Create ephemeral key for client-side Stripe SDK
    ephemeral_key = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2024-04-10',
    )
    
    # Create payment intent
    payment_intent = stripe.PaymentIntent.create(
        amount=prices.get(price_id, 0),  # Get price from the dictionary or default to 0
        currency='usd',
        customer=customer['id'],
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={'user_id': user_id, 'plan_id': price_id}  # Add metadata for later use
    )
    
    if not payment_intent or not ephemeral_key:
        return {
            "error": "Failed to create payment intent"
        }

    return json.dumps({
        "paymentIntent": payment_intent.client_secret,
        "ephemeralKey": getattr(ephemeral_key, "secret", None),
        "customer": customer.id,
        "publishableKey": STRIPE_PUBLISHABLE_KEY
    })
