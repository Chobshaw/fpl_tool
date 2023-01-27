from dependency_injector import containers, providers
from pymongo import MongoClient

from helpers.mongodb_helper import MongodbHelper
from models.settings_model import StandaloneSettings


class StandaloneContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[StandaloneSettings()])

    # Gateways
    mongo_client = providers.Singleton(
        MongoClient,
        config.MONGODB_CONNECTION_STRING
    )

    # Databases
    fixture_history_collection = providers.Singleton(
        MongodbHelper,
        client=mongo_client,
        database_name=config.TEAM_DATA_DATABASE_NAME,
        collection_name=config.FIXTURE_HISTORY_COLLECTION_NAME
    )
