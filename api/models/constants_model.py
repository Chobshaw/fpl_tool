from pydantic import BaseModel

from models.mongodb_base_model import MongodbBaseModel


class FixtureDataLoaderConstants(BaseModel):
    competition_codes_dict: dict[str, str]
    fixture_data_url: str
    column_name_dict: dict[str, str]


class Constants(MongodbBaseModel):
    fixture_data_loader_constants: FixtureDataLoaderConstants
