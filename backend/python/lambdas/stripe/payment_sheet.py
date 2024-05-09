import json
from src.Classes.User import DatabaseSyncedProfile
import stripe

stripe.api_key = 'sk_test_51PCbyWRpgjuWcdPRWkDUKRRShKb8lZiYKQP8Ov37s2TdaAAGJYB4kteMHmiTHU7aBM40IoNbejAgMjRtn2wR4jDJ00gazKtd1m'

def handler(event, context):
    userId = event['userId']
    priceId = event['planId']
    prices: dict[str, int] = {
        'plan_premium': 2999,
        'plan_exclusive': 5999,
        'plan_standard': 1499
    }
    user = DatabaseSyncedProfile.from_id(userId)
    if user and user.stripe_customer_id:
        customer = stripe.Customer.retrieve(user.stripe_customer_id)
    else:
        customer = stripe.Customer.create()
        user.stripe_customer_id = customer.id

    ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2024-04-10',
      )
    paymentIntent = stripe.PaymentIntent.create(
        amount=prices[priceId] or int(priceId.split('_')[1]), # users can also buy credits
        currency='usd',
        customer=customer['id'],
        automatic_payment_methods={
          'enabled': True,
        },
      )


           
    if "plan_" in priceId:
        user.expiry_date = None
    elif "credits_" in priceId: 
        print("Credits aren't integrated yet!")

    return json.dumps({"paymentIntent": paymentIntent.client_secret,
                 "ephemeralKey": ephemeralKey.secret,
                 "customer": customer.id,
                 "publishableKey": 'pk_test_51PCbyWRpgjuWcdPRNb5nGYKleCCaDgtnAEcidL7x8CEwR7jkYicsAM2DCHwmZO7CsKE0uYFPocH974I1xtHdDseP004I8LUgiT'})

