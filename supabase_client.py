from os import getenv
from supabase import create_client, Client
from dotenv import load_dotenv

from fastapi import WebSocket
import asyncio
import json

load_dotenv()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

supabase_url = getenv('SUPABASE_URL')
supabase_key = getenv('SUPABASE_KEY')
supabase_service_key = getenv('SUPABASE_SERVICE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)
manager = ConnectionManager()

async def fetch_votes():
    response = await supabase.table("Votes").select("*").execute()
    return response.data if response.data else []

