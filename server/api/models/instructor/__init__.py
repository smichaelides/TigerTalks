# api/models/instructor.py
from bson import ObjectId
from typing import Optional
from server.api.models._base import Model


class Instructor(Model):
    _id: ObjectId
    emplid: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
