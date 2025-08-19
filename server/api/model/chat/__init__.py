from server.api.model._base import Model
from server.api.model.message import UserMessage, ModelMessage
from server.api.model.user import User


class Chat(Model):
    user_messages: list[UserMessage]
    model_messages: list[ModelMessage]
    user: User