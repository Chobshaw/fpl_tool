import itertools
import posixpath
from datetime import datetime

import pandas as pd

from helpers.mongodb_helper import MongodbHelper
from helpers.parameter_store_helper import ParameterStoreHelper
from models.fixture_history_model import FixtureHistoryItems
from utils.converters import written_to_snake, str_to_hex_id, fixture_date_to_datetime
from utils.data_loaders import load_csv_to_df_from_url


class FixtureDataLoaderService:
    def __init__(self, mongodb_helper: MongodbHelper, parameter_store_helper: ParameterStoreHelper) -> None:
        self.mongodb_helper = mongodb_helper
        self.constants = parameter_store_helper.constants.fixture_data_loader_constants

    def format_fixture_data(self, df: pd.DataFrame, season: int) -> pd.DataFrame:
        df = df[self.constants.column_name_dict.keys()]
        df.dropna(inplace=True)
        df.rename(columns=self.constants.column_name_dict, inplace=True)
        df['competition'] = df['competition'].map(
            {code: competition for competition, code in self.constants.competition_codes_dict.items()}
        )
        df['date'] = df['date'].map(fixture_date_to_datetime)
        df[['team_home', 'team_away']] = df[['team_home', 'team_away']].applymap(written_to_snake)
        df.insert(0, 'season', f'{season}-{season + 1}')
        df['code'] = df.apply(lambda row: str_to_hex_id(f'{row.date}-{row.team_home}-{row.team_away}'), axis=1)
        return df

    def load_historical_fixture_data_to_mongodb(self, from_year: int, to_year: int, competitions: list[str]):
        competition_codes = [self.constants.competition_codes_dict[competition] for competition in competitions]
        suffix = '.csv'
        for season, competition in itertools.product(range(from_year, to_year + 1), competition_codes):
            print(season, competition)
            season_fixture_data_url = posixpath.join(
                self.constants.fixture_data_url, f'{str(season)[2:]}{str(season + 1)[2:]}', competition + suffix
            )
            fixture_history_df = load_csv_to_df_from_url(season_fixture_data_url)
            fixture_history_df = self.format_fixture_data(fixture_history_df, season)
            fixture_history_items = FixtureHistoryItems(items=fixture_history_df.to_dict('records'))
            self.mongodb_helper.batch_put_items(
                items=fixture_history_items.dict()['items']
            )
