from pydantic import BaseSettings, Field


class APISettings(BaseSettings):
    MONGODB_CONNECTION_STRING: str = Field(env='MONGODB_CONNECTION_STRING')
    TEAM_DATA_DATABASE_NAME: str = Field(env='TEAM_DATA_DATABASE_NAME')
    FIXTURE_HISTORY_COLLECTION_NAME: str = Field(env='FIXTURE_HISTORY_COLLECTION_NAME')

    class Config:
        case_sensitive = True


class StandaloneSettings(APISettings):
    FIXTURE_DATA_URL: str = Field(env='FIXTURE_DATA_URL')
