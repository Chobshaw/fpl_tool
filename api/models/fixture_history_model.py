from datetime import datetime

from bson import ObjectId
from pandas._libs import NaTType
from pydantic import BaseModel, Field


class FixtureHistoryItem(BaseModel):
    id: ObjectId = Field(None, alias='_id')
    code: int
    game_week: float
    season_fixture_id: int
    timestamp: datetime | NaTType
    team_h: int
    team_a: int
    team_h_score: int | float
    team_a_score: int | float

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class FixtureHistoryItems(BaseModel):
    items: list[FixtureHistoryItem]
