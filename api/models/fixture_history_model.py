from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel


class FixtureHistoryItem(BaseModel):
    _id: Optional[ObjectId] = None
    code: int
    game_week: float
    season_fixture_id: int
    timestamp: datetime
    team_h: int
    team_a: int
    team_h_score: int | float
    team_a_score: int | float

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class FixtureHistoryItems(BaseModel):
    items: list[FixtureHistoryItem]
