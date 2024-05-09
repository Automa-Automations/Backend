
from supabase import create_client, Client

url: str = "https://wvzgejpisuukgnohsimu.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2emdlanBpc3V1a2dub2hzaW11Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMzMyMzA5NCwiZXhwIjoyMDI4ODk5MDk0fQ.OXmy2LfFyQJpZRqmediQblCNGVioRAM9dI8TlEoY-0o"
supabase: Client = create_client(url, key)


