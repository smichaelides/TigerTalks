import logging
from datetime import datetime, timezone
from bson import ObjectId
from flask import Blueprint, request
from server.database import get_database
from server.api.models.chat import Chat
from server.api.models.message import UserMessage, ModelMessage

chat = Blueprint("chat", __name__, url_prefix="/chat")


@chat.route("/create-chat", methods=["POST"])
def create_chat():
    db = get_database()
    payload = request.get_json()

    assert "user_id" in payload

    new_chat = Chat(
        user_id=ObjectId(payload.get("user_id")), user_messages=[], model_messages=[]
    )

    try:
        db.chats.insert_one(new_chat.model_dump())
    except Exception as ex:
        logging.error("Failed to create a new chat: %s", ex)
        return {"error": f"Failed to create a new chat {ex}"}, 500

    return new_chat.model_dump_json(), 201


@chat.route("/send-message", methods=["POST"])
def send_message():
    db = get_database()
    payload = request.get_json()

    assert "chat_id" in payload
    assert "user_id" in payload
    assert "timestamp" in payload

    payload["chat_id"] = ObjectId(payload["chat_id"])
    payload["user_id"] = ObjectId(payload["user_id"])
    payload["timestamp"] = datetime.now(tz=timezone.utc)

    user_msg = UserMessage.model_validate(payload)

    try:
        db.chats.update_one(
            {"_id": user_msg.chat_id},
            {"$push": {"user_messages": user_msg.model_dump()}},
        )
    except Exception as ex:
        logging.error("Failed to upload user message to the database: %s", ex)
        return {"error": f"Failed to upload user message to the database: {ex}"}, 500

    model_msg = ModelMessage.model_validate(payload)
    model_msg.message = (
        "This is a simulated response. The backend integration will be added later!"
    )
    try:
        db.chats.update_one(
            {"_id": model_msg.chat_id},
            {"$push": {"model_messages": model_msg.model_dump()}},
        )
    except Exception as ex:
        logging.error("Failed to upload model message to the database: %s", ex)
        return {"error": f"Failed to upload model message to the database: {ex}"}, 500

    return {"model_message": model_msg.message}, 201
