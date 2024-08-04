import json
import os


def handler(event, context):
    print(event)

    env_type = "LOCAL_"
    if os.environ.get("CURRENT_ENVIRONMENT", "local") == "prod":
        env_type = "HOSTED_"

    supabase_url = os.environ[env_type + "SUPABASE_URL"]
    supabase_key = os.environ[env_type + "SUPABASE_ANON_KEY"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"supabase_url": supabase_url, "supabase_key": supabase_key}
        ),
    }
