from dataclasses import dataclass

import pandas as pd


@dataclass
class Team:
    name: str
    league: str
    history: pd.DataFrame
