from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from models.mongodb_base_model import MongodbBaseModel


class MatchDay(BaseModel):
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
    history: list[MatchDay]
    # squad_history: list[SquadUpdate]
