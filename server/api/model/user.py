from bson import ObjectId
from server.api.model._base import Model


class User(Model):
    _id: ObjectId
