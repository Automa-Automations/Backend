
from supabase import create_client, Client
import os

print(os.environ)
url: str = os.getenv("HOSTED_SUPABASE_URL", "") if os.getenv("CURRENT_ENVIRONMENT", "local") == "prod" else os.getenv("LOCAL_SUPABASE_URL", "local")
key: str = os.getenv("HOSTED_SUPABASE_SERVICE_KEY", "") if os.getenv("CURRENT_ENVIRONMENT", "local") == "prod" else os.getenv("HOSTED_SUPABASE_SERVICE_KEY", "local")
supabase: Client = create_client(url, key)


