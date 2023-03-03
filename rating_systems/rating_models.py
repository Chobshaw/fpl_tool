from datetime import datetime, MINYEAR, timedelta
from itertools import chain, product
from pathlib import Path
from typing import Optional, Protocol, NamedTuple, Literal

import numpy as np
import pandas as pd

from models.rating_model_parameters import EloModelParameters
from models.team_model import TeamInstance, TeamDict
from rating_systems.elo import EloCalculator


class Scores(NamedTuple):
    mean_absolute_error: float
    mean_squared_error: float


class RatingModel(Protocol):
    def fit(self, fixtures_df: pd.DataFrame, team_dict: dict[str, list[TeamInstance]]):
        ...

    def rate(
            self, fixtures_df: pd.DataFrame, team_dict: dict[str, list[TeamInstance]], reverse_rate: bool = False
    ) -> Scores:
        ...


class EloModel:
    def __init__(self, saved_model_path: Optional[str] = None):
        if saved_model_path is None:
            saved_model_path = Path(__file__).parents[1] / 'api\\saved_models\\elo_model_parameters.json'
        self.parameters = EloModelParameters.parse_file(saved_model_path)
        self.team_dict: Optional[TeamDict] = None
        self.elo_calculator = EloCalculator(
            k_factor=self.parameters.k_factor,
            constant=self.parameters.elo_constant,
            home_advantage=self.parameters.home_advantage,
            ha_evolution_rate=self.parameters.ha_evolution_rate
        )
        self.promoted_teams = set()
        self.promoted_team_elo = self.parameters.default_ratings_dict['championship']

    def fit(self, fixtures_df: pd.DataFrame, team_dict: dict[str, list[TeamInstance]]):
        k_min, k_max = self.parameters.k_factor_limits
        return

    def _get_current_elo(self, team: str, competition: str) -> float:
        if team in self.promoted_teams:
            self.promoted_teams.remove(team)
            return self.promoted_team_elo
        elif len(self.team_dict[team]) == 0:
            return self.parameters.default_ratings_dict[competition]
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

    @staticmethod
    def _get_scores(fixtures_df: pd.DataFrame, no_of_years: Optional[int] = None) -> Scores:
        if no_of_years is None:
            start_date = datetime(year=2000, month=1, day=1)
        else:
            start_date = fixtures_df.date.iloc[-1] - timedelta(days=365 * no_of_years)
        mae, mse = fixtures_df[fixtures_df.date >= start_date].apply(
            lambda x: x['result_home'] - x['expected_result_home'], axis=1
        ).agg(
            [lambda x: sum(abs(x)) / len(x), lambda x: sum(x ** 2) / len(x)]
        )
        return Scores(mean_absolute_error=mae, mean_squared_error=mse)

    def rate(
            self,
            fixtures_df: pd.DataFrame,
            team_dict: TeamDict,
            reverse_rate: bool = False
    ) -> Scores:
        self.team_dict = team_dict
        fixtures_df['expected_result_home'] = 0
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
            elo_home_new, elo_away_new = self.elo_calculator.calculate_new_elos(
                elo_home=elo_home,
                elo_away=elo_away,
                score_home=fixture.goals_home,
                score_away=fixture.goals_away
            )
            fixtures_df.loc[fixture.Index, 'expected_result_home'] = self.elo_calculator.expected_score
            self.team_dict[fixture.team_home].append(self._get_new_team_instance(fixture, 'home', elo_home_new))
            self.team_dict[fixture.team_away].append(self._get_new_team_instance(fixture, 'away', elo_away_new))
        for team, team_instances in self.team_dict.items():
            start_index = 0
            for i in range(len(team_instances) - 1):
                if team_instances[i + 1].date <= team_instances[i].date:
                    start_index = i + 1
            self.team_dict[team] = team_instances[start_index:]
        return self._get_scores(fixtures_df)
