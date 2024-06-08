import json
from src.Classes.Plan import Plan
from src.Classes.User import DatabaseSyncedProfile
import stripe
import traceback
from typing import Optional
import os

stripe.api_key = os.environ["STRIPE_API_KEY"]
STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]

def handler(event, context):
    print(event)
    body = json.loads(event["body"])
    print(body)
    user_id = body["userId"]
    price_id = body["planId"]

    user = DatabaseSyncedProfile.from_id(user_id)
    customer: Optional[stripe.Customer] = None
    if user and user.stripe_customer_id:
        try:
            customer = stripe.Customer.retrieve(user.stripe_customer_id)
        except stripe.StripeError as e:
            print(
                "Failed to retrieve customer",
                e,
                traceback.format_exc(),
                user.stripe_customer_id,
            )
            customer = None

    if not customer:
        customer = stripe.Customer.create()
        user.stripe_customer_id = customer.id

    ephemeral_key = stripe.EphemeralKey.create(
        customer=customer["id"],
        stripe_version="2024-04-10",
    )

    payment_intent = stripe.PaymentIntent.create(
        amount=int(Plan.from_id(price_id).price * 100),
        currency="usd",
        customer=customer["id"],
        automatic_payment_methods={
            "enabled": True,
        },
        metadata={"user_id": user_id, "plan_id": price_id},
    )

    if not payment_intent or not ephemeral_key:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Failed to create payment intent"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "paymentIntent": payment_intent.client_secret,
                "ephemeralKey": getattr(ephemeral_key, "secret", None),
                "customer": customer.id,
                "publishableKey": STRIPE_PUBLISHABLE_KEY,
            }
        ),
    }
