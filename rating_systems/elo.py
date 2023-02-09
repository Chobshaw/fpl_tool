class EloCalculator:
    def __init__(self, k_factor: int = 32, constant: int = 400, ) -> None:
        self.k_factor = k_factor
        self.constant = constant
        self.prediction_error = None

    def calculate_expected_score(self, elo_home: float, elo_away: float):
        return 1 / (1 + 10 ** ((elo_away - elo_home) / self.constant))

    def _get_prediction_error(self, elo_home: float, elo_away: float, score_home: int, score_away: int) -> float:
        actual_score = int(score_home > score_away) + 0.5 * int(score_home == score_away)
        self.expected_score = self.calculate_expected_score(elo_home, elo_away)
        return actual_score - self.expected_score

    def calculate_new_elos(
            self, elo_home: float, elo_away: float, score_home: int, score_away: int
    ) -> tuple[float, float]:
        self.prediction_error = self._get_prediction_error(elo_home, elo_away, score_home, score_away)
        elo_change = self.k_factor * self.prediction_error
        return elo_home + elo_change, elo_away - elo_change
