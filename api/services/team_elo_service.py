from datetime import datetime

from helpers.mongodb_helper import MongodbHelper
from models.fixture_history_model import FixtureHistoryItems
from models.mongodb_query_model import MongodbQueryModel, TableKey


class TeamEloService:
    def __init__(self, mongodb_helper: MongodbHelper):
        self.mongodb_helper = mongodb_helper

    def _get_fixture_data(self, from_timestamp: datetime, to_timestamp: datetime):
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
        pass

    def calculate_elo_data(self):
        self._get_fixture_data()
