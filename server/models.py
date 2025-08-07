from pydantic import BaseModel
from typing import Optional, Dict, Any


# Server I/O Models
class Event(BaseModel):
    uuid: str
    event: str
    properties: Dict[str, Any]

class ChatQueryInput(BaseModel):
    text: str
    uuid: str
    session_id: str

class Feedback(BaseModel):
    uuid: str
    session_id: str
    msg_index: int
    feedback: Optional[str] = None

# Tool Models - TO BE IMPLEMENTED LATER 

# Memory Models - TO BE IMPLEMENTED LATER