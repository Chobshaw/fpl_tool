from pydantic import BaseSettings, Field


class APISettings(BaseSettings):
    MONGODB_CONNECTION_STRING: str = Field(env='MONGODB_CONNECTION_STRING')
    PARAMETER_STORE_DATABASE_NAME: str = Field(env='PARAMETER_STORE_DATABASE_NAME')
    PARAMETERS_COLLECTION_NAME: str = Field(env='PARAMETERS_COLLECTION_NAME')
    TEAM_DATA_DATABASE_NAME: str = Field(env='TEAM_DATA_DATABASE_NAME')
    FIXTURES_COLLECTION_NAME: str = Field(env='FIXTURES_COLLECTION_NAME')
    TEAM_INSTANCES_COLLECTION_NAME: str = Field(env='TEAM_INSTANCES_COLLECTION_NAME')

    class Config:
        case_sensitive = True


class StandaloneSettings(APISettings):
    pass
