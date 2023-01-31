from dependency_injector import containers, providers
from pymongo import MongoClient

from helpers.mongodb_helper import MongodbHelper
from helpers.parameter_store_helper import ParameterStoreHelper
from models.settings_model import StandaloneSettings
from services.fixture_data_loader_service import FixtureDataLoaderService


class StandaloneContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[StandaloneSettings()])

    # Gateways
    mongo_client = providers.Singleton(
        MongoClient,
        config.MONGODB_CONNECTION_STRING
    )

    # Databases
    parameter_store_mongodb_helper = providers.Singleton(
        MongodbHelper,
        client=mongo_client,
        database_name=config.PARAMETER_STORE_DATABASE_NAME,
        collection_name=config.PARAMETERS_COLLECTION_NAME
    )

    parameter_store_helper = providers.Singleton(
        ParameterStoreHelper,
        mongodb_helper=parameter_store_mongodb_helper
    )

    fixture_history_mongodb_helper = providers.Singleton(
        MongodbHelper,
        client=mongo_client,
        database_name=config.TEAM_DATA_DATABASE_NAME,
        collection_name=config.FIXTURE_HISTORY_COLLECTION_NAME
    )

    # Services
    data_loader_service = providers.Factory(
        FixtureDataLoaderService,
        mongodb_helper=fixture_history_mongodb_helper,
        parameter_store_helper=parameter_store_helper
    )
