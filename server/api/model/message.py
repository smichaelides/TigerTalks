from datetime import datetime
from bson import ObjectId
from server.api.model._base import Model


class Message(Model):
    _id: ObjectId
    message: str
    timestamp: datetime


class UserMessage(Message):
    user_id: str


class ModelMessage(Message):
    model_id: str
