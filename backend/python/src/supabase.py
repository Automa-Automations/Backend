
from supabase import create_client, Client

url: str = "https://wvzgejpisuukgnohsimu.supabase.co"
key: str = "TODO: Create environment variables file for these!"
supabase: Client = create_client(url, key)


