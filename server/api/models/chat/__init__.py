from datetime import datetime
from server.api.models._base import Model
from server.api.models.message import UserMessage, ModelMessage


class Chat(Model):
    title: str = "New Chat"
    userMessages: list[UserMessage]
    modelMessages: list[ModelMessage]
    createdAt: datetime
    updatedAt: datetime
    userId: str
