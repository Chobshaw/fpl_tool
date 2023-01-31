from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class MongodbBaseModel(BaseModel):
    _id: Optional[ObjectId] = None

    class Config:
        arbitrary_types_allowed = True
