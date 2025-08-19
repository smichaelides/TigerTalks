import os
import logging
from flask import g
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

CONNECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]
DATABASE_NAME = os.environ["DATABASE_NAME"]


def get_database():
    if 'db' not in g:
        client: MongoClient[dict[str, object]] = MongoClient(CONNECTION_STRING)

        try:
            client.admin.command("ping")
            logging.info("Connected to MongoDB; using database %s", DATABASE_NAME)
            g.db = client[DATABASE_NAME]
        except Exception as ex:
            logging.error(
                "An error occurred while creating the database client: %s", ex
            )
            raise

    return g.db
