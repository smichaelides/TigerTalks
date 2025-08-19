from datetime import datetime
from bson import ObjectId
from server.api.model._base import Model
from server.api.model.user import User


class Message(Model):
    _id: ObjectId
    chat_id: ObjectId
    message: str
    timestamp: datetime


class UserMessage(Message):
    user: User


class ModelMessage(Message):
    message: str = (
        "This is a simulated response. The backend integration will be added later!"
    )
