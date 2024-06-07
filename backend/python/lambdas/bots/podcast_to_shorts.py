import json
import os
from src.Classes.Bots import PodcastToShorts


def handler(event, context):
    env_type = "LOCAL_"
    if os.environ.get("CURRENT_ENVIRONMENT", "local") == "prod":
        env_type = "HOSTED_"

    return {
        "statusCode": 200,
        "body": json.dumps({"hello": "123"}),
    }
