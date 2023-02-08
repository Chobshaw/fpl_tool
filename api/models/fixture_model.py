from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from models.mongodb_base_model import MongodbBaseModel


class MatchResult(float, Enum):
    WIN = 1.0
    DRAW = 0.5
    LOSS = 0.0


class Fixture(MongodbBaseModel):
    code: str
    competition: str
    season: str
    date: datetime
    team_home: str
    team_away: str
    goals_home: int
    goals_away: int
    result_home: MatchResult


class FixtureList(BaseModel):
    items: list[Fixture]
