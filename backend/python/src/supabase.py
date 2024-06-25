from supabase import create_client
import os

print(os.environ)
url: str = os.getenv("HOSTED_SUPABASE_URL", "") if os.getenv("CURRENT_ENVIRONMENT", "local") == "prod" else os.getenv("LOCAL_SUPABASE_URL", "local")
key: str = os.getenv("HOSTED_SUPABASE_SERVICE_KEY", "") if os.getenv("CURRENT_ENVIRONMENT", "local") == "prod" else os.getenv("HOSTED_SUPABASE_SERVICE_KEY", "local")
print("URL", url, "KEY", key)
supabase = create_client(url, key)


