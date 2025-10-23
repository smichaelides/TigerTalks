import logging
from bson import ObjectId
from flask import Blueprint, request
from server.api.models.user import User
from server.database import get_database

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/get-user", methods=["GET"])
def get_user():
    db = get_database()
    user_id = request.args.get("userId")

    try:
        db_user = db.users.find_one({"_id": ObjectId(user_id)})
        if not db_user:
            return {"error": f"User with id {user_id} not found"}, 404
        # expose string id to the model via public 'id' field and avoid touching protected attributes
        db_user["id"] = str(db_user["_id"])
        fetched_user = User.model_validate(db_user)
    except Exception as ex:
        logging.error("Failed to get user %s: %s", user_id, ex)
        return {"error": f"Failed to get user {user_id}"}, 500

    # expose original MongoDB _id as string in the response
    result = fetched_user.model_dump()
    result["_id"] = str(db_user["_id"])
    return result, 200

@user.route("/get-user-by-email", methods=["GET"])
def get_user_by_email():
    db = get_database()
    email = request.args.get("email")

    try:
        db_user = db.users.find_one({"email": email})
        if not db_user:
            return {"error": f"User with email {email} not found"}, 404
        # expose string id to the model via public 'id' field and avoid touching protected attributes
        db_user["id"] = str(db_user["_id"])
        fetched_user = User.model_validate(db_user)
    except Exception as ex:
        logging.error("Failed to get user %s: %s", email, ex)
        return {"error": f"Failed to get user {email}"}, 500

    # expose original MongoDB _id as string in the response
    result = fetched_user.model_dump()
    result["_id"] = str(db_user["_id"])
    return result, 200


@user.route("/create-user", methods=["POST"])
def create_user():
    db = get_database()
    payload = request.get_json()

    if "name" not in payload:
        return {"error": "Missing required field: name"}, 400
    if "email" not in payload:
        return {"error": "Missing required field: email"}, 400

    new_user = User(
        _id=payload.get("email"),
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

    if "userId" not in payload:
        return {"error": "Missing required field: userId"}, 400
    if "concentration" not in payload:
        return {"error": "Missing required field: concentration"}, 400

    userId: str = payload.get("userId")
    concentration: str = payload.get("concentration")

    try:
        db.users.update_one(
            {"_id": ObjectId(userId)}, {"$set": {"concentration": concentration}}
        )
    except Exception as ex:
        logging.error(
            "Failed to update concentration {%s} for user %s: %s",
            concentration,
            userId,
            ex,
        )
        return {"error": f"Failed to update concentration {concentration}."}, 500

    return {"concentration": concentration}, 200


@user.route("/update-certificates", methods=["PATCH"])
def update_certificates():
    db = get_database()
    payload = request.get_json()

    if "userId" not in payload:
        return {"error": "Missing required field: userId"}, 400
    if "certificates" not in payload:
        return {"error": "Missing required field: certificates"}, 400

    userId: str = payload.get("userId")
    certificates: list[str] = payload.get("certificates")

    try:
        db.users.update_one(
            {"_id": ObjectId(userId)}, {"$set": {"certificates": certificates}}
        )
    except Exception as ex:
        logging.error(
            "Failed to update certificates {%s} for user %s: %s",
            certificates,
            userId,
            ex,
        )
        return {"error": f"Failed to update certificates {certificates}."}, 500

    return {"certificates": certificates}, 200
