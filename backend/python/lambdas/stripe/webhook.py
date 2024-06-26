import json
from src.Classes.Plan import Plan
from src.Classes.User import DatabaseSyncedProfile
import stripe
import os

stripe.api_key = os.environ["STRIPE_API_KEY"]


def handle_stripe_event(event):
    print(event)
    body = json.loads(event["body"])
    print(body)
    event_data = body["data"]["object"]
    if event_data["object"] == "charge":
        user_id = event_data["metadata"]["user_id"]
        price_id = event_data["metadata"]["plan_id"]

        user = DatabaseSyncedProfile.from_id(user_id)

        if "plan_" in price_id:
            user.expiry_date = None
            user.plan_type = price_id
            plan = Plan.from_id(price_id)
            user.credits += plan.credits
        elif "credits_" in price_id:
            print("Credits integration pending!")


def handler(event, context):
    handle_stripe_event(event)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Webhook received successfully"}),
    }
