from typing import Any

from pydantic import BaseModel


class TableKey(BaseModel):
    name: str
    value: Any
    aux_value: Any = None


class MongodbQueryModel(BaseModel):
    index_key: TableKey
