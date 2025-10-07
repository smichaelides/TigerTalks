from datetime import datetime
from bson import ObjectId
from server.api.models._base import Model


class Message(Model):
    chatId: ObjectId
    message: str
    timestamp: datetime


class UserMessage(Message):
    userId: str


class ModelMessage(Message):
    message: str = (
        "This is a simulated response. The backend integration will be added later!"
    )
