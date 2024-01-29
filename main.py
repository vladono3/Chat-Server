from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from contacts.contacts import contacts_router
from discussions.discussions import discussions_router
from users.users import users_router
from messages.messages import message_router
from websocket.manager import ConnectionManager



app = FastAPI()
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(discussions_router)
app.include_router(message_router)
manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    await manager.update()
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(message, [client_id])
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_id)
        await manager.update()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
