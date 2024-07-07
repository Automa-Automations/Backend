import json
import datetime
from src.Classes.Plan import Plan
from src.Classes.User import DatabaseSyncedProfile
from src.Classes.CreditTransaction import CreditTransaction
import stripe
import os
import uuid

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
        print('credits_' in price_id)
        print(price_id, user_id)
        if "plan_" in price_id:
            user.expiry_date = None
            user.plan_type = price_id
            plan = Plan.from_id(price_id)
            user.credits += plan.credits
            CreditTransaction(id=uuid.uuid4().hex, user_id=user.id, credits=plan.credits, metadata=event_data, head="Purchased Plan", created_at=datetime.datetime.now()).add()
        elif "credits_" in price_id:

            print("Credits integration pending!")
            credits = int(price_id.split("_")[1])
            print(credits)
            user.credits += credits
            CreditTransaction(id=uuid.uuid4().hex, user_id=user.id, credits=credits, metadata={"stripe_charge_id": event_data['id']}, head="Purchased Credits", created_at=datetime.datetime.now()).add()


def handler(event, context):
    handle_stripe_event(event)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Webhook received successfully"}),
    }
