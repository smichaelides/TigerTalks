from bson import ObjectId
from server.api.models._base import Model
from server.api.models.message import UserMessage, ModelMessage


class Chat(Model):
    user_messages: list[UserMessage]
    model_messages: list[ModelMessage]
    user_id: ObjectId