from datetime import datetime
from typing import DefaultDict

from pydantic import BaseModel

from models.mongodb_base_model import MongodbBaseModel


class TeamInstance(MongodbBaseModel):
    team: str
    competition: str
    date: datetime
    elo: float
    # elo_attack: float
    # elo_defense: float


TeamDict = DefaultDict[str, list[TeamInstance]]


class Team(BaseModel):
    name: str
    team_instances: list[TeamInstance]
