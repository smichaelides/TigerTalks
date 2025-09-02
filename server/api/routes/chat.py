import logging
from typing import Any
from datetime import datetime, timezone
from bson import ObjectId
from flask import Blueprint, request
from server.database import get_database
from server.api.models.chat import Chat
from server.api.models.message import UserMessage, ModelMessage

chat = Blueprint("chat", __name__, url_prefix="/chat")


@chat.route("/get-chat", methods=["GET"])
def get_chat():
    db = get_database()
    chat_id = request.args.get("chat_id")
    user_id = request.args.get("user_id")

    if chat_id is None:
        return {"error": "Missing required fields: 'chat_id' and 'user_id'."}, 400

    if user_id is None:
        return {"error": "Missing required fields: 'chat_id' and 'user_id'."}, 400

    try:
        chat_dict: dict[str, str | list[dict[str, str]]] | None | Any = (
            db.chats.find_one(
                {
                    "_id": ObjectId(chat_id),
                    "user_id": ObjectId(user_id),
                }
            )
        )
        if not chat_dict:
            return {"error": "Chat not found."}, 404

        # Convert ObjectId fields to strings for JSON serialization
        chat_dict["_id"] = str(chat_dict["_id"])
        chat_dict["user_id"] = str(chat_dict["user_id"])

        for key in ["user_messages", "model_messages"]:
            if isinstance(chat_dict[key], list):
                for msg in chat_dict[key]:
                    if isinstance(msg, dict) and isinstance(msg["user_id"], ObjectId):
                        msg["user_id"] = str(msg["user_id"])
                    if isinstance(msg, dict) and isinstance(msg["chat_id"], ObjectId):
                        msg["chat_id"] = str(msg["chat_id"])
    except Exception as ex:
        logging.exception("Error retrieving chat data: %s", ex)
        return {"error": "Error retrieving chat data."}, 500

    return {"chat": chat_dict}, 200


@chat.route("/list-chats", methods=["GET"])
def list_chats():
    db = get_database()
    user_id = request.args.get("user_id")

    if user_id is None:
        return {"error": "Missing required field: 'user_id'."}, 400

    try:
        chats = list(db.chats.find({"user_id": ObjectId(user_id)}, {"_id": 1}))
        # only lists out the _id, we can call /get-chat to get the messages
        for chat_dict in chats:
            chat_dict["_id"] = str(chat_dict["_id"])
    except Exception as ex:
        logging.exception("Error retrieving chats: %s", ex)
        return {"error": "Error retrieving chats."}, 500

    return {"chats": chats}, 200


@chat.route("/create-chat", methods=["POST"])
def create_chat():
    db = get_database()
    payload = request.get_json()

    if "user_id" not in payload:
        return {"error": "Missing required field: 'user_id'."}, 400

    # Verify that user_id exists in the users collection
    try:
        user_exists = db.users.find_one({"_id": ObjectId(payload.get("user_id"))})
        if not user_exists:
            logging.error(
                "User with user_id %s does not exist.", payload.get("user_id")
            )
            return {"error": "Invalid user_id. User does not exist."}, 400
    except Exception as ex:
        logging.error("Failed to verify user existence: %s", ex)
        return {"error": f"Failed to verify user existence: {ex}"}, 500

    new_chat = Chat(
        user_id=ObjectId(payload.get("user_id")), user_messages=[], model_messages=[]
    )

    try:
        chat_id = db.chats.insert_one(new_chat.model_dump()).inserted_id
    except Exception as ex:
        logging.error("Failed to create a new chat: %s", ex)
        return {"error": f"Failed to create a new chat {ex}"}, 500

    new_chat.chat_id = str(chat_id)
    return new_chat.model_dump_json(), 201


@chat.route("/send-message", methods=["POST"])
def send_message():
    db = get_database()
    payload = request.get_json()

    if not payload:
        return {"error": "Payload is missing."}, 400

    if "chat_id" not in payload:
        return {"error": "Missing required field: 'chat_id'."}, 400

    if "user_id" not in payload:
        return {"error": "Missing required field: 'user_id'."}, 400

    if "timestamp" not in payload:
        return {"error": "Missing required field: 'timestamp'."}, 400

    payload["chat_id"] = ObjectId(payload["chat_id"])
    payload["user_id"] = ObjectId(payload["user_id"])
    payload["timestamp"] = datetime.now(tz=timezone.utc)

    user_msg = UserMessage.model_validate(payload)

    try:
        result = db.chats.update_one(
            {"_id": user_msg.chat_id, "user_id": user_msg.user_id},
            {"$push": {"user_messages": user_msg.model_dump()}},
        )
        if result.matched_count == 0:
            logging.error(
                "No chat found matching chat_id and user_id: %s", user_msg.chat_id
            )
            return {"error": "No chat found matching chat_id and user_id."}, 404
    except Exception as ex:
        logging.error("Failed to upload user message to the database: %s", ex)
        return {"error": f"Failed to upload user message to the database: {ex}"}, 500

    model_msg = ModelMessage.model_validate(payload)
    model_msg.message = (
        "This is a simulated response. The backend integration will be added later!"
    )
    try:
        db.chats.update_one(
            {"_id": model_msg.chat_id, "user_id": user_msg.user_id},
            {"$push": {"model_messages": model_msg.model_dump()}},
        )
    except Exception as ex:
        logging.error("Failed to upload model message to the database: %s", ex)
        return {"error": f"Failed to upload model message to the database: {ex}"}, 500

    return {"model_message": model_msg.message}, 201
