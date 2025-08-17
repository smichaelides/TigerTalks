import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

CONNECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]
DATABASE_NAME = os.environ["DATABASE_NAME"]


def get_database():
    client: MongoClient[dict[str, object]] = MongoClient(CONNECTION_STRING)

    try:
        logging.info("Creating database client for %s", DATABASE_NAME)
        database = client[DATABASE_NAME]
    except Exception as ex:
        logging.error("An error occurred while creating the database client: %s", ex)
        raise

    return database
