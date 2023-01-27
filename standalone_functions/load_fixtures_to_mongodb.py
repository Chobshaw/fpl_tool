from datetime import datetime

from dependency_injector.wiring import Provide, inject

from containers.standalone_containers import Container
from helpers.mongodb_helper import MongodbHelper
from models.fixture_history_model import FixtureHistoryItems
from utils.data_loaders import load_df_from_url


@inject
def load_fixtures_to_mongodb(fixture_history_collection: MongodbHelper = Provide[Container.fixture_history_collection]):
    fixture_history_df = load_df_from_url('https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2022-23/fixtures.csv')
    used_columns = ['code', 'event', 'id', 'kickoff_time', 'team_a', 'team_a_score', 'team_h', 'team_h_score']
    fixture_history_df = fixture_history_df[used_columns]
    fixture_history_df.dropna(subset=['kickoff_time'], inplace=True)
    column_name_dict = {
        'event': 'game_week',
        'id': 'season_fixture_id',
        'kickoff_time': 'timestamp'
    }
    fixture_history_df.rename(columns=column_name_dict, inplace=True)
    fixture_history_df['timestamp'] = fixture_history_df['timestamp'].map(
        lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
    )
    fixture_history_items = FixtureHistoryItems(items=fixture_history_df.to_dict('records'))
    fixture_history_collection.batch_replace_items(
        items=fixture_history_items.dict()['items'],
        filter_field='code'
    )


def main():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    load_fixtures_to_mongodb()


main()
