import dotenv
import os

dotenv.load_dotenv('../../.env')



# from src.Classes.User import DatabaseSyncedProfile
# import datetime
#
#
# user: DatabaseSyncedProfile = DatabaseSyncedProfile.from_id("a68c5905-205d-43e3-8bbb-0b6c87aea79e")
# # Loop over all properties of the user
# for key, value in user.__dict__.items():
#     print(f"{key}: {value}")
#
# user.full_name = "John0Doe" # Invalid
# print(user.full_name)
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
#\
# from lambdas.stripe.payment_sheet import handler as payment_sheet
# print(payment_sheet({'resource': '/payment-sheet', 'path': '/payment-sheet', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '37611', 'CloudFront-Viewer-Country': 'ZA', 'Content-Type': 'application/json', 'Host': 'ia4csru8sj.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'python-requests/2.31.0', 'Via': '1.1 1db4ab20ef3897e534041f147e869cca.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'f4XX0UDe_CH0lrRsK2LUk93Ec9tRvfPcvhIG0tJpk5FEiaggfZ9m0g==', 'X-Amzn-Trace-Id': 'Root=1-663e8cd8-4e5ba6634bd1c71826008184', 'X-Forwarded-For': '169.0.3.162, 130.176.145.152', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['37611'], 'CloudFront-Viewer-Country': ['ZA'], 'Content-Type': ['application/json'], 'Host': ['ia4csru8sj.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['python-requests/2.31.0'], 'Via': ['1.1 1db4ab20ef3897e534041f147e869cca.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['f4XX0UDe_CH0lrRsK2LUk93Ec9tRvfPcvhIG0tJpk5FEiaggfZ9m0g=='], 'X-Amzn-Trace-Id': ['Root=1-663e8cd8-4e5ba6634bd1c71826008184'], 'X-Forwarded-For': ['169.0.3.162, 130.176.145.152'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'hafc3s', 'resourcePath': '/payment-sheet', 'httpMethod': 'POST', 'extendedRequestId': 'Xkrx6FaMIAMEQEg=', 'requestTime': '10/May/2024:21:08:40 +0000', 'path': '/prod/payment-sheet', 'accountId': '471112943852', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': 'ia4csru8sj', 'requestTimeEpoch': 1715375320721, 'requestId': 'fe9068e4-0cd0-459d-a3a9-9e21484712f8', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '169.0.3.162', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'python-requests/2.31.0', 'user': None}, 'domainName': 'ia4csru8sj.execute-api.us-east-1.amazonaws.com', 'deploymentId': '1pw1kd', 'apiId': 'ia4csru8sj'}, 'body': '{"userId": "a68c5905-205d-43e3-8bbb-0b6c87aea79e", "planId": "plan_standard"}', 'isBase64Encoded': False}, None))
#
#
# from lambdas.config.auto_config_mobile_app import handler as auto_config_mobile_app
# print(auto_config_mobile_app({'resource': '/payment-sheet', 'path': '/payment-sheet', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '37611', 'CloudFront-Viewer-Country': 'ZA', 'Content-Type': 'application/json', 'Host': 'ia4csru8sj.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'python-requests/2.31.0', 'Via': '1.1 1db4ab20ef3897e534041f147e869cca.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'f4XX0UDe_CH0lrRsK2LUk93Ec9tRvfPcvhIG0tJpk5FEiaggfZ9m0g==', 'X-Amzn-Trace-Id': 'Root=1-663e8cd8-4e5ba6634bd1c71826008184', 'X-Forwarded-For': '169.0.3.162, 130.176.145.152', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['37611'], 'CloudFront-Viewer-Country': ['ZA'], 'Content-Type': ['application/json'], 'Host': ['ia4csru8sj.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['python-requests/2.31.0'], 'Via': ['1.1 1db4ab20ef3897e534041f147e869cca.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['f4XX0UDe_CH0lrRsK2LUk93Ec9tRvfPcvhIG0tJpk5FEiaggfZ9m0g=='], 'X-Amzn-Trace-Id': ['Root=1-663e8cd8-4e5ba6634bd1c71826008184'], 'X-Forwarded-For': ['169.0.3.162, 130.176.145.152'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'hafc3s', 'resourcePath': '/payment-sheet', 'httpMethod': 'POST', 'extendedRequestId': 'Xkrx6FaMIAMEQEg=', 'requestTime': '10/May/2024:21:08:40 +0000', 'path': '/prod/payment-sheet', 'accountId': '471112943852', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': 'ia4csru8sj', 'requestTimeEpoch': 1715375320721, 'requestId': 'fe9068e4-0cd0-459d-a3a9-9e21484712f8', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '169.0.3.162', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'python-requests/2.31.0', 'user': None}, 'domainName': 'ia4csru8sj.execute-api.us-east-1.amazonaws.com', 'deploymentId': '1pw1kd', 'apiId': 'ia4csru8sj'}, 'body': '{"userId": "a68c5905-205d-43e3-8bbb-0b6c87aea79e", "planId": "plan_standard"}', 'isBase64Encoded': False}, None))
#
# from lambdas.bots.image_poster import *
# if __name__ == "__main__":
#     base_prompt = "Cute cats, bright and colorful landscapes, Usage of humanlike behaviours, cute eyes, bliss, loving and kind personality."
#     current_topic = "The topic for the image should be of a random animal, preferrably cats, alligators, dogs, pandas, ducks, bears. It should be an animal name, with a prefix and or suffix, which will make it more descriptive and will not obstruct the image generation!"
#     base_style = "playful, puffy, smooth, cute, 4k, --rtx"
#     title_style = "The title should be in a cute and playful style, with a lot of emojis and a lot of exclamation marks Also include 3-4 hashtags in the title that will perform well."
#     negative_prompt = "Text, Watermark, hands, ugly, dark, gloomy, sad, depressing, scary, horror, nightmare, creepy, spooky, evil, mean, angry, mad, rage, hate, violence, blood, gore"
#     image_size = (1080, 1080)
#     total_images = 1
#     model = "realisticVisionV60B1_v51VAE.safetensors"
#     new_topic = generate_topic_item(base_topic=current_topic)
#     new_prompt = generate_image_prompt(base_prompt=base_prompt, topic=new_topic, style=base_style)
#     print("Topic:", new_topic, "\nPrompt:", new_prompt)
#     images = generate_image(new_prompt, negative_prompt, model, image_size)
#     # Save each image with random uuid and print
#     upload_image("a68c5905-205d-43e3-8bbb-0b6c87aea79e", images, generate_image_title(title_style, new_topic, base_style))
#

# from src.Classes.Bots.AiImageGenerator import Instagram
# #
# bot = Instagram.from_id(1, type_=Instagram)
# title, topic, prompt, description, images = bot.generate()
# bot.upload(title, topic, prompt, description, images)
# print(bot)



from src.Classes.Bot import InstagramPlatformBot

bot = InstagramPlatformBot.from_id(1, type_=InstagramPlatformBot)
print(bot.configuration)
bot.modify_schedule('posting_interval', "* * * * *")

# bot.upload()

