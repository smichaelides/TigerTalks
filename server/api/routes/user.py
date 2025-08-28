import logging
from bson import ObjectId
from flask import Blueprint, request
from server.api.models.user import User
from server.database import get_database

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/get-user", methods=["GET"])
def get_user():
    db = get_database()
    user_id = request.args.get("user_id")

    try:
        db_user = db.users.find_one({"_id": ObjectId(user_id)})
        fetched_user = User.model_validate(db_user)
    except Exception as ex:
        logging.error("Failed to get user %s: %s", user_id, ex)
        return {"error": f"Failed to get user {user_id}"}, 500

    return fetched_user.model_dump_json(), 200


@user.route("/create-user", methods=["POST"])
def create_user():
    db = get_database()
    payload = request.get_json()

    if "name" not in payload:
        return {"error": "Missing required field: name"}, 400
    if "email" not in payload:
        return {"error": "Missing required field: email"}, 400

    new_user = User(
        name=payload.get("name"),
        email=payload.get("email"),
        grad_year=payload.get("grad_year"),
        concentration=payload.get("concentration"),
        certificates=payload.get("certificates", []),
    )

    try:
        db.users.insert_one(new_user.model_dump())
    except Exception as ex:
        logging.error("Failed to create new user: %s", ex)
        return {"error": "Failed to create new user"}, 500

    return new_user.model_dump_json(), 201


@user.route("/update-concentration", methods=["PATCH"])
def update_concentration():
    db = get_database()
    payload = request.get_json()

    if "user_id" not in payload:
        return {"error": "Missing required field: user_id"}, 400
    if "concentration" not in payload:
        return {"error": "Missing required field: concentration"}, 400

    user_id: str = payload.get("user_id")
    concentration: str = payload.get("concentration")

    try:
        db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"concentration": concentration}}
        )
    except Exception as ex:
        logging.error(
            "Failed to update concentration {%s} for user %s: %s",
            concentration,
            user_id,
            ex,
        )
        return {"error": f"Failed to update concentration {concentration}."}, 500

    return {"concentration": concentration}, 200


@user.route("/update-certificates", methods=["PATCH"])
def update_certificates():
    db = get_database()
    payload = request.get_json()

    if "user_id" not in payload:
        return {"error": "Missing required field: user_id"}, 400
    if "certificates" not in payload:
        return {"error": "Missing required field: certificates"}, 400

    user_id: str = payload.get("user_id")
    certificates: list[str] = payload.get("certificates")

    try:
        db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"certificates": certificates}}
        )
    except Exception as ex:
        logging.error(
            "Failed to update certificates {%s} for user %s: %s",
            certificates,
            user_id,
            ex,
        )
        return {"error": f"Failed to update certificates {certificates}."}, 500

    return {"certificates": certificates}, 200
