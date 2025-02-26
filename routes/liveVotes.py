from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from supabase_client import supabase

router = APIRouter()

# Store connected clients
clients = []

async def broadcast():
    """Broadcast data to all connected clients every 3 seconds."""
    while True:
        data = supabase.table('Votes').select("*").execute().data
        for client in clients:
            await client.send_json(data)
        await asyncio.sleep(3)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        clients.remove(websocket)

# Start the broadcast loop
@router.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast())