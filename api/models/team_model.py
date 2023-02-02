from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from models.mongodb_base_model import MongodbBaseModel


class TeamInstance(BaseModel):
    team_name: str
    competition: str
    date: datetime
    elo: float
    # elo_attack: float
    # elo_defense: float


class SquadUpdate(BaseModel):
    date: datetime
    players: list[str]


class TeamModel(MongodbBaseModel):
    name: str
    league: Literal['premier_league', 'championship']
    history: list[TeamInstance]
    # squad_history: list[SquadUpdate]
