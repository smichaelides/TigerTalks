# internal imports
from datetime import datetime

# external imports
from pydantic import BaseModel


class Message(BaseModel):
    message: str
    message_id: str
    conversation_id: str
    timestamp: datetime


class UserMessage(Message):
    user_id: str


class ModelMessage(Message):
    model_id: str
