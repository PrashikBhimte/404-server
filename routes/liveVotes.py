# connection_manager.py
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

# Active WebSocket connections
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
            await connection.send_text(message)


# supabase_service.py
from supabase import create_client, Client
import json
import asyncio
from connection_manager import ConnectionManager

# Supabase configuration
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
manager = ConnectionManager()

async def fetch_and_broadcast_votes():
    last_votes = None
    while True:
        response = supabase.table("election_votes").select("candidate_id, votes").execute()
        votes = response.data
        votes_json = json.dumps(votes)
        
        if votes_json != last_votes:  # Only broadcast if data changes
            await manager.broadcast(votes_json)
            last_votes = votes_json
        
        await asyncio.sleep(5)  # Poll every 5 seconds


# main.py
from fastapi import FastAPI, WebSocket
from supabase_service import fetch_and_broadcast_votes, manager
import asyncio

# FastAPI app
app = FastAPI()

@app.websocket("/ws/votes")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Start the background task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_and_broadcast_votes())
