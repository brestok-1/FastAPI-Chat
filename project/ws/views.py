from fastapi import WebSocket, WebSocketDisconnect

from . import ws_router
from .consumer import manager


@ws_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data['text'], data['username'], data['created_at'])
    except WebSocketDisconnect:
        manager.disconnect(websocket)


