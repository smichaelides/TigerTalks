from bson import ObjectId
from server.api.models._base import Model


class User(Model):
    _id: ObjectId
