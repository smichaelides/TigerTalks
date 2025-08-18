from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        extra="allow",  # still need to decide if we want this, or "ignore"
        str_strip_whitespace=True,
    )
