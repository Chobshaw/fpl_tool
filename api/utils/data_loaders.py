import io

import pandas as pd
import requests


def load_df_from_url(url: str) -> pd.DataFrame:
    response = requests.get(url)
    byte_content = io.BytesIO(response.content)
    return pd.read_csv(byte_content)
