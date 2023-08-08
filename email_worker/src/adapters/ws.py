from websockets.server import WebSocketServerProtocol
from models.ws import Connection


class WS:
    def __init__(self) -> None:
        self.connections: list[Connection] = []

    async def register(self, websocket: WebSocketServerProtocol) -> None:
        user_id = await websocket.recv()
        self.connections.append(
            Connection(user_id=user_id, websocket=websocket)
        )

    async def notify(self, message: str, user_id: str) -> None:
        user_connections = [
            i for i in self.connections
            if i.user_id == user_id
        ]
        if user_connections is None:
            return

        for i in user_connections:
            await i.websocket.send(message)
