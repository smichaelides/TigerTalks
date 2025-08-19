import logging
from flask import Blueprint, request
from server.api.model.user import User
from server.database import get_database

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/create-user", methods=["POST"])
def create_user():
    logging.info("/create-user called")
    db = get_database()
    payload = request.get_json()

    assert "name" in payload
    assert "email" in payload
    assert "grad_year" in payload

    new_user = User(
        name=payload.get("name"),
        email=payload.get("email"),
        grad_year=payload.get("grad_year"),
        concentration=payload.get("concentration"),
        certificates=payload.get("certificates", [])
    )

    try:
        db.users.insert_one(new_user.model_dump())
    except Exception as ex:
        logging.error("Failed to create new user: %s", ex)
        return {"error": f"Failed to create new user: {ex}"}, 500

    return new_user.model_dump_json(), 201
