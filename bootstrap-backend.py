import json
import boto3
import stripe
import dotenv
import subprocess
import os

dotenv.load_dotenv()

def create_stripe_webhook(url: str, enabled_events: list = ["charge.succeeded", "charge.failed"], description: str ="Some Description", route: str = "webhook"):
    try:
        webhook_endpoint = stripe.WebhookEndpoint.create(
            enabled_events=enabled_events,
            url=url+f'/{route}',
            description=description
        )
        print("Webhook created successfully:")
        print(json.dumps(webhook_endpoint, indent=2))
    except stripe.StripeError as e:
        print("Failed to create webhook:", str(e))


def get_aws_api_gateway(api_name: str):
    # Create a Boto3 client for API Gateway
    client = boto3.client('apigateway')

    # List all REST APIs
    response = client.get_rest_apis()

    # Extract information about each API
    apis = response['items']
    for api in apis:
        # Return the URL if it has the same name
        if api['name'] == api_name:
            # Retrieve the region
            region = client.meta.region_name
            # Return the URL with the region
            return f"https://{api['id']}.execute-api.{region}.amazonaws.com/prod"

    return ""

def bootstrap_stripe(stripe_api_key: str):
    import stripe
    stripe.api_key = stripe_api_key
    stripe_api_url = get_aws_api_gateway("backend-generic-api")
    print(stripe_api_url)

    create_stripe_webhook(stripe_api_url, ['charge.succeeded'], "Stripe Payment Success Webhook", 'stripe/webhook')

def bootstrap_supabase():
    subprocess.run(["npx", "supabase", "stop"])
    subprocess.run(["npx", "supabase", "start"])
    subprocess.run(["npx", "supabase", "login"])
    subprocess.run(["npx", "supabase", "init"])
    subprocess.run(["npx", "supabase", "link", "--project-ref", os.getenv("SUPABASE_PROJECT_REF", "")])
    subprocess.run(["npx", "supabase", "migration", "up"])


def deploy_cdk_project():
    subprocess.run(["sudo", "cdk", "deploy"])

if __name__ == "__main__":
    dotenv.set_key(".env", "API_BASE_URL", get_aws_api_gateway("backend-generic-api"))

    deploy_cdk_project()
    bootstrap_supabase()
    bootstrap_stripe(os.getenv("STRIPE_API_KEY", ""))
