from enum import Enum
from typing import List, Optional, Dict, Any
from clients import db_client
import time

class MessageType(Enum):
    HUMAN = "human"
    AI = "ai"

class ToolInvocation:
    def __init__(self, tool: str, input: str, output: str):
        self.tool = tool
        self.input = input
        self.output = output

    def to_dict(self) -> Dict[str, str]:
        return {
            "tool": self.tool,
            "input": self.input,
            "output": self.output
        }

class Memory:
    def __init__(self, uuid: str, session_id: str, last_n: int = 10):
        self.uuid = uuid
        self.session_id = session_id
        self.last_n = last_n
        self.conversations = db_client["conversations"]
        self._messages_cache = None  # Cache for recent messages

    def _message_to_str(self, message: Dict[str, Any]) -> str:
        """Convert a message to a string format for context"""
        msg_str = f"{message['type']}: {message['content']}"
        if 'tool_use' in message and message['tool_use']:
            tool_use = message['tool_use']
            msg_str += f" [Tool: {tool_use['tool']}]"
        return msg_str

    def get_messages(self) -> List[str]:
        """Get recent messages as formatted strings for context"""
        messages = self.get_recent_messages()
        return [self._message_to_str(msg) for msg in messages]

    def get_recent_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get recent messages from database"""
        if limit is None:
            limit = self.last_n
            
        # Try cache first
        if self._messages_cache is not None:
            return self._messages_cache[-limit:]
        
        # Query database
        conversation = self.conversations.find_one(
            {"uuid": self.uuid, "session_id": self.session_id},
            {"messages": {"$slice": -limit}}
        )
        
        if conversation:
            messages = conversation.get("messages", [])
            # Update cache
            self._messages_cache = messages
            return messages
        return []

    def add_message(self, message_type: MessageType, content: str, tool_use: Optional[ToolInvocation] = None):
        """Add a new message to the conversation"""
        timestamp = int(time.time())
        
        message = {
            "type": message_type.value,
            "content": content,
            "timestamp": timestamp
        }
        
        if tool_use:
            message["tool_use"] = tool_use.to_dict()
        
        # Update database
        self.conversations.update_one(
            {"uuid": self.uuid, "session_id": self.session_id},
            {
                "$push": {"messages": message},
                "$set": {"last_updated": timestamp}
            },
            upsert=True
        )
        
        # Update cache
        if self._messages_cache is not None:
            self._messages_cache.append(message)
            # Keep cache size manageable
            if len(self._messages_cache) > self.last_n * 2:
                self._messages_cache = self._messages_cache[-self.last_n:]

    def clear_cache(self):
        """Clear the message cache (useful for testing or memory management)"""
        self._messages_cache = None

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary information about the conversation"""
        conversation = self.conversations.find_one(
            {"uuid": self.uuid, "session_id": self.session_id}
        )
        
        if not conversation:
            return {"message_count": 0, "last_updated": None}
        
        messages = conversation.get("messages", [])
        return {
            "message_count": len(messages),
            "last_updated": conversation.get("last_updated"),
            "session_id": self.session_id,
            "uuid": self.uuid
        }
