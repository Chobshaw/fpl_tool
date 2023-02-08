from typing import Any

from pydantic import BaseModel, Field


class IndexKey(BaseModel):
    name: str
    value: Any
    aux_value: Any = None


class MongodbQueryModel(BaseModel):
    partition_key: IndexKey = None
    sort_key: IndexKey = None
