from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from supabase_client import fetch_and_broadcast_votes, manager
import asyncio

router = APIRouter()

@router.websocket("/ws/votes")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await fetch_and_broadcast_votes()
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

