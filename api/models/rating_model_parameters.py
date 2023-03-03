from pydantic import BaseModel


class EloModelParameters(BaseModel):
    default_ratings_dict: dict[str, int]
    k_factor: int
    elo_constant: int
    home_advantage: float
    ha_evolution_rate: float
    k_factor_limits: tuple[int, int]
    elo_constant_limits: tuple[int, int]
