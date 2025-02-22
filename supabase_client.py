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

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)

supabase_url = getenv('SUPABASE_URL')
supabase_key = getenv('SUPABASE_KEY')
supabase_service_key = getenv('SUPABASE_SERVICE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)
manager = ConnectionManager()

async def fetch_and_broadcast_votes():
    last_votes = None
    while True:
        response = supabase.table("Votes").select("*").execute()
        votes = response.data
        votes_json = json.dumps(votes)
        
        if votes_json != last_votes: 
            await manager.broadcast(votes_json)
            last_votes = votes_json
        
        await asyncio.sleep(5)