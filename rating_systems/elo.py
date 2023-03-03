import math


class EloCalculator:
    def __init__(
            self, k_factor: int = 32, constant: int = 400, home_advantage: float = 50, ha_evolution_rate: float = 0.075
    ) -> None:
        self.k_factor = k_factor
        self.constant = constant
        self.home_advantage = home_advantage
        self.ha_evolution_rate = ha_evolution_rate
        self.expected_score = None
        self.prediction_error = None

    def calculate_expected_score(self, elo_home: float, elo_away: float):
        return 1 / (1 + 10 ** ((elo_away - elo_home - self.home_advantage) / self.constant))

    def _get_prediction_error(self, elo_home: float, elo_away: float, score_home: int, score_away: int) -> float:
        actual_score = int(score_home > score_away) + 0.5 * int(score_home == score_away)
        self.expected_score = self.calculate_expected_score(elo_home, elo_away)
        return actual_score - self.expected_score

    def calculate_new_elos(
            self, elo_home: float, elo_away: float, score_home: int, score_away: int
    ) -> tuple[float, float]:
        self.prediction_error = self._get_prediction_error(elo_home, elo_away, score_home, score_away)
        # score_difference_factor = abs(score_home - score_away) ** 1/2
        # score_difference_factor = math.log10(1 + abs(score_home - score_away)) / math.log10(2)
        score_difference_factor = min(sum(0.5 ** (i - 1) for i in range(1, abs(score_home - score_away))), 1)
        # score_difference_factor = 1
        elo_change = self.k_factor * score_difference_factor * self.prediction_error
        self.home_advantage += self.ha_evolution_rate * elo_change
        return elo_home + elo_change, elo_away - elo_change
