from bson import ObjectId
from server.api.model._base import Model
from server.api.model.message import UserMessage, ModelMessage
from server.api.model.user import User


class Chat(Model):
    conversation_id: ObjectId
    user_messages: list[UserMessage]
    model_messages: list[ModelMessage]
    users: list[User]
