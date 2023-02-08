from datetime import datetime

from pydantic import BaseModel

from models.mongodb_base_model import MongodbBaseModel


class Fixture(MongodbBaseModel):
    code: str
    competition: str
    season: str
    date: datetime
    team_home: str
    team_away: str
    goals_home: int
    goals_away: int


class FixtureList(BaseModel):
    items: list[Fixture]