from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = (
    os.environ.get("HOSTED_SUPABASE_URL", "")
    if os.environ.get("CURRENT_ENVIRONMENT", "local") == "prod"
    else os.environ.get("LOCAL_SUPABASE_URL", "local")
)
key: str = (
    os.environ.get("HOSTED_SUPABASE_SERVICE_KEY", "")
    if os.environ.get("CURRENT_ENVIRONMENT", "local") == "prod"
    else os.environ.get("HOSTED_SUPABASE_SERVICE_KEY", "local")
)
supabase: Client = create_client(url, key)
