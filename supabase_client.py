from os import getenv
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase_url = getenv('SUPABASE_URL')
supabase_key = getenv('SUPABASE_KEY')
supabase_service_key = getenv('SUPABASE_SERVICE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)