from datetime import datetime
from typing import Optional

import pandas as pd

from helpers.mongodb_helper import MongodbHelper
from models.fixture_history_model import FixtureHistoryItems
from models.mongodb_query_model import MongodbQueryModel, TableKey
from models.team_model import TeamInstance


class TeamEloService:
    def __init__(self, mongodb_helper: MongodbHelper):
        self.mongodb_helper = mongodb_helper

    def _get_fixture_data(self, from_timestamp: datetime, to_timestamp: datetime) -> pd.DataFrame:
        response = self.mongodb_helper.query_items_between(
            mongodb_query_model=MongodbQueryModel(
                index_key=TableKey(
                    name='date',
                    value=from_timestamp,
                    aux_value=to_timestamp
                )
            )
        )
        fixture_history_items = FixtureHistoryItems.parse_obj(response)
        return pd.DataFrame.from_records(fixture_history_items.dict()['items'])

    def _get_most_recent_match_day(self, team_name: str, from_timestamp: datetime) -> Optional[TeamInstance]:
        pass

    def _get_teams(self, team_names: list[str], from_timestamp: datetime) -> dict[str, list[TeamInstance]]:
        for name in team_names:
            match_day = self._get_most_recent_match_day(team_name=name, from_timestamp=from_timestamp)
            if match_day is None:
                pass


    def calculate_elo_data(self, from_timestamp: datetime, to_timestamp: datetime):
        fixture_history_df = self._get_fixture_data(from_timestamp, to_timestamp)
        team_names = list(set(fixture_history_df['team_home'].unique()) | set(fixture_history_df['team_away'].unique()))
        teams = self._get_teams(team_names=team_names)
