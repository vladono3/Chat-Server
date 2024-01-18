from starlette.websockets import *
from contacts.contacts import get_contact


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    async def disconnect(self, websocket: WebSocket, client_id):
        self.active_connections.pop(client_id)

    async def broadcast(self, message, contacts):
        for contact in contacts:
            connection = self.active_connections.get(contact)
            if connection:
                await connection.send_json(message)

    async def update(self):
        connection_dict = {
            "type": "connections",
            "ids": list(self.active_connections.keys())
        }
        for connection in self.active_connections.values():
            if connection:
                await connection.send_json(connection_dict)

