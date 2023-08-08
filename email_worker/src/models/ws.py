import uuid

from websockets.server import WebSocketServerProtocol
from sqlmodel import Field
from src.models.base import BaseOrjsonModel


class Connection(BaseOrjsonModel):
    user_id: str
    connection_id: uuid = Field(default_factory=uuid.uuid4)
    websocket: WebSocketServerProtocol
