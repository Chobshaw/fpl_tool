from collections import defaultdict
from datetime import datetime
from typing import Optional, DefaultDict

import pandas as pd

from helpers.mongodb_helper import MongodbHelper
from models.constants_model import TeamRatingServiceConstants
from models.fixture_model import FixtureList
from models.mongodb_query_model import MongodbQueryModel, IndexKey
from models.team_model import TeamInstance
from rating_systems.rating_models import RatingModel


class TeamRatingService:
    def __init__(
            self,
            fixtures_collection: MongodbHelper,
            team_instances_collection: MongodbHelper,
            constants: TeamRatingServiceConstants,
            rater: RatingModel
    ) -> None:
        self.fixtures_collection = fixtures_collection
        self.team_instances_collection = team_instances_collection
        self.constants = constants
        self.rater = rater

    def _get_fixture_data(self, from_timestamp: datetime, to_timestamp: datetime) -> pd.DataFrame:
        response = self.fixtures_collection.query_items_between(
            mongodb_query_model=MongodbQueryModel(
                sort_key=IndexKey(
                    name='date',
                    value=from_timestamp,
                    aux_value=to_timestamp
                )
            )
        )
        fixtures = FixtureList.parse_obj(response)
        return pd.DataFrame.from_records(fixtures.dict()['items'])

    def _get_most_recent_match_day(self, team_name: str, from_timestamp: datetime) -> Optional[TeamInstance]:
        return

    def _get_teams(self, team_names: list[str], from_timestamp: datetime) -> DefaultDict[str, list[TeamInstance]]:
        team_dict = defaultdict(list)
        for name in team_names:
            match_day = self._get_most_recent_match_day(team_name=name, from_timestamp=from_timestamp)
            if match_day is None:
                continue
            team_dict[name] = [match_day]
        return team_dict

    def get_team_ratings(self, from_timestamp: datetime, to_timestamp: datetime):
        fixtures_df = self._get_fixture_data(from_timestamp, to_timestamp)
        team_names = list(set(fixtures_df['team_home'].unique()) | set(fixtures_df['team_away'].unique()))
        teams = self._get_teams(team_names=team_names, from_timestamp=from_timestamp)
        scores = self.rater.score(fixtures_df=fixtures_df, team_dict=teams, reverse_rate=True)
        pass
