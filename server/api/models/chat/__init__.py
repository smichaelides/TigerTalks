from datetime import datetime
from server.api.models._base import Model
from server.api.models.message import UserMessage, ModelMessage


class Chat(Model):
    user_messages: list[UserMessage]
    model_messages: list[ModelMessage]
    created_at: datetime
    updated_at: datetime
    user_id: str
