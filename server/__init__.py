import os

from dotenv import load_dotenv
from flask import Flask
from server.api.routes import register_routes

from server.database import get_database_client

load_dotenv()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        MONGODB_CONNECTION_STRING=os.getenv("MONGODB_CONNECTION_STRING"),
        DATABASE_NAME=os.getenv("DATABASE_NAME"),
    )

    # Create and attach one DB handle for the whole process
    setattr(
        app,
        "mongo_db",
        get_database_client(),
    )

    register_routes(app)

    return app
