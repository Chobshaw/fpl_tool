import json
from itertools import chain
from pathlib import Path
from typing import Optional, Protocol, NamedTuple, Literal

import numpy as np
import pandas as pd

from models.team_model import TeamInstance, TeamDict
from rating_systems.elo import EloCalculator


class Scores(NamedTuple):
    mean_absolute_error: float
    mean_squared_error: float


class RatingModel(Protocol):
    def fit(self, fixtures_df: pd.DataFrame, team_dict: dict[str, list[TeamInstance]]):
        ...

    def rate(self, fixtures_df: pd.DataFrame, team_dict: dict[str, list[TeamInstance]], reverse_rate: bool = False):
        ...

    def score(self, fixtures_df: pd.DataFrame, team_dict: TeamDict, reverse_rate: bool = False):
        ...


class EloModel:
    def __init__(self, saved_model_path: Optional[str] = None):
        self.default_ratings_dict: Optional[dict[str, int]] = None
        if saved_model_path is None:
            saved_model_path = Path(__file__).parents[1] / 'api\\saved_models\\elo_model_parameters.json'
        self.load(saved_model_path)
        self.team_dict: Optional[TeamDict] = None
        self.promoted_teams = set()
        self.promoted_team_elo = self.default_ratings_dict['championship']

    def load(self, path: str):
        with open(path, 'r') as file:
            saved_model_parameters = json.load(file)
        for key, val in saved_model_parameters.items():
            setattr(self, key, val)

    def fit(self, fixtures_df: pd.DataFrame, team_dict: dict[str, list[TeamInstance]]):
        pass

    def _get_current_elo(self, team: str, competition: str) -> float:
        if team in self.promoted_teams:
            self.promoted_teams.remove(team)
            return self.promoted_team_elo
        elif len(self.team_dict[team]) == 0:
            return self.default_ratings_dict[competition]
        else:
            return self.team_dict[team][-1].elo

    @staticmethod
    def _get_new_team_instance(
            fixture: NamedTuple, home_or_away: Literal['home', 'away'], new_elo: float
    ) -> TeamInstance:
        team = fixture.team_home if home_or_away == 'home' else fixture.team_away
        return TeamInstance(
            team=team,
            competition=fixture.competition,
            date=fixture.date,
            elo=new_elo
        )

    def rate(self, fixtures_df: pd.DataFrame, team_dict: TeamDict, reverse_rate: bool = False) -> None:
        self.team_dict = team_dict
        fixtures_df['expected_result_home'] = 0
        elo_calculator = EloCalculator(k_factor=64)
        current_season = fixtures_df.loc[0, 'season']
        if reverse_rate:
            fixtures_iterator = chain(
                fixtures_df.itertuples(), reversed(list(fixtures_df.itertuples())), fixtures_df.itertuples()
            )
        else:
            fixtures_iterator = fixtures_df.itertuples()
        for fixture in fixtures_iterator:
            if fixture.season != current_season:
                old_teams = set(fixtures_df.loc[fixtures_df['season'] == current_season, 'team_home'].unique())
                new_teams = set(fixtures_df.loc[fixtures_df['season'] == fixture.season, 'team_home'].unique())
                relegated_teams = old_teams.difference(new_teams)
                self.promoted_teams = new_teams.difference(old_teams)
                self.promoted_team_elo = np.mean([self.team_dict[team][-1].elo for team in relegated_teams])
                current_season = fixture.season
            elo_home = self._get_current_elo(fixture.team_home, fixture.competition)
            elo_away = self._get_current_elo(fixture.team_away, fixture.competition)
            elo_home_new, elo_away_new = elo_calculator.calculate_new_elos(
                elo_home=elo_home,
                elo_away=elo_away,
                score_home=fixture.goals_home,
                score_away=fixture.goals_away
            )
            fixtures_df.loc[fixture.Index, 'expected_result_home'] = elo_calculator.expected_score
            self.team_dict[fixture.team_home].append(self._get_new_team_instance(fixture, 'home', elo_home_new))
            self.team_dict[fixture.team_away].append(self._get_new_team_instance(fixture, 'away', elo_away_new))
        for team, team_instances in self.team_dict.items():
            start_index = 0
            for i in range(len(team_instances) - 1):
                if team_instances[i + 1].date <= team_instances[i].date:
                    start_index = i + 1
            self.team_dict[team] = team_instances[start_index:]
        pass

    def score(self, fixtures_df: pd.DataFrame, team_dict: TeamDict, reverse_rate: bool = False) -> Scores:
        self.rate(fixtures_df, team_dict, reverse_rate)
        mae, mse = fixtures_df.apply(lambda x: x['result_home'] - x['expected_result_home'], axis=1).agg(
            [lambda x: sum(abs(x)) / len(x), lambda x: sum(x ** 2) / len(x)]
        )
        return Scores(mean_absolute_error=mae, mean_squared_error=mse)
