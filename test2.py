import boto3

def list_apis():
    # Create a Boto3 client for API Gateway
    client = boto3.client('apigateway')

    # List all REST APIs
    response = client.get_rest_apis()

    # Extract information about each API
    apis = response['items']
    for api in apis:
        print(f"API Name: {api['name']}")
        print(f"API ID: {api['id']}")
        print()

if __name__ == "__main__":
    list_apis()
