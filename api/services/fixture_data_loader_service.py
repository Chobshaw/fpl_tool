import itertools
import posixpath

import pandas as pd

from helpers.mongodb_helper import MongodbHelper
from models.constants_model import FixtureDataLoaderConstants
from models.fixture_model import FixtureList
from utils.converters import written_to_snake, str_to_hex_id, fixture_date_to_datetime
from utils.data_loaders import load_csv_to_df_from_url


class FixtureDataLoaderService:
    def __init__(self, fixtures_collection: MongodbHelper, constants: FixtureDataLoaderConstants) -> None:
        self.fixtures_collection = fixtures_collection
        self.constants = constants

    def format_fixture_data(self, df: pd.DataFrame, season: int) -> pd.DataFrame:
        df = df[self.constants.column_name_dict.keys()]
        df.dropna(inplace=True)
        df.rename(columns=self.constants.column_name_dict, inplace=True)
        df['competition'] = df['competition'].map(
            {code: competition for competition, code in self.constants.competition_codes_dict.items()}
        )
        df['date'] = df['date'].map(fixture_date_to_datetime)
        df[['team_home', 'team_away']] = df[['team_home', 'team_away']].applymap(written_to_snake)
        df['result_home'] = df.apply(
            lambda x: int(x['goals_home'] > x['goals_away']) + 0.5 * int(x['goals_home'] == x['goals_away']),
            axis=1
        )
        df.insert(0, 'season', f'{season}-{season + 1}')
        df['code'] = df.apply(lambda row: str_to_hex_id(f'{row.date}-{row.team_home}-{row.team_away}'), axis=1)
        return df

    def load_fixture_data_to_mongodb(self, from_year: int, to_year: int, competitions: list[str]):
        competition_codes = [self.constants.competition_codes_dict[competition] for competition in competitions]
        suffix = '.csv'
        for season, competition in itertools.product(range(from_year, to_year + 1), competition_codes):
            print(season, competition)
            season_fixture_data_url = posixpath.join(
                self.constants.fixture_data_url, f'{str(season)[2:]}{str(season + 1)[2:]}', competition + suffix
            )
            fixtures_df = load_csv_to_df_from_url(season_fixture_data_url)
            fixtures_df = self.format_fixture_data(fixtures_df, season)
            fixtures = FixtureList(items=fixtures_df.to_dict('records'))
            self.fixtures_collection.batch_replace_items(
                items=fixtures.dict()['items'],
                filter_field='code'
            )
