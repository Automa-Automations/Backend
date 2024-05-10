# from src.Classes.User import DatabaseSyncedProfile
# import datetime
#
# user: DatabaseSyncedProfile = DatabaseSyncedProfile.from_id("a68c5905-205d-43e3-8bbb-0b6c87aea79e")
# # Loop over all properties of the user
# for key, value in user.__dict__.items():
#     print(f"{key}: {value}")
#
# # user.full_name = "John0Doe" # Invalid
# # print(user.full_name)
#
# user.full_name = "John Doe"
# print(user.full_name)
#
# user.avatar_url = "https://source.unsplash.com/random/300×300"
# print(user.avatar_url)
#
# user.website = "https://somerandomwebsite.com"
# print(user.website)
#
# user.expiry_date = datetime.datetime.now() + datetime.timedelta(days=10000)
# print(user.expiry_date)
#
# user.stripe_customer_id = "gus_123456868686"
# print(user.stripe_customer_id)
#

from lambdas.stripe.payment_sheet import handler as payment_sheet

print(payment_sheet({
    "userId": "a68c5905-205d-43e3-8bbb-0b6c87aea79e",
    "planId": "plan_standard"
}, None))
