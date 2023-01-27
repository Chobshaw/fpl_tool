from datetime import datetime

from dependency_injector.wiring import Provide, inject

from containers.standalone_containers import StandaloneContainer
from helpers.mongodb_helper import MongodbHelper
from models.fixture_history_model import FixtureHistoryItems
from utils.data_loaders import load_df_from_url


def season_generator(from_season: int, to_season: int) -> str:
    # TODO: Add "inclusive" argument to specify whether the interval precisely
    for season in range(from_season, to_season):
        yield f'{season}-{str(season + 1)}'


@inject
def load_fixtures_to_mongodb(
        fixture_history_collection: MongodbHelper = Provide[StandaloneContainer.fixture_history_collection],
        fixture_data_url: str = Provide[StandaloneContainer.config.FIXTURE_DATA_URL]
):
    split_url = fixture_data_url.split('season')
    for season in season_generator(2018, 2023):
        fixture_data_url_for_season = (season[:5] + season[-2:]).join(split_url)
        fixture_history_df = load_df_from_url(fixture_data_url_for_season)
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
        fixture_history_df.insert(0, 'season', season)
        fixture_history_items = FixtureHistoryItems(items=fixture_history_df.to_dict('records'))
        fixture_history_collection.batch_update_items(
            items=fixture_history_items.dict()['items'],
            filter_field='code',
            update_field='season'
        )


def main():
    container = StandaloneContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    load_fixtures_to_mongodb()


main()
