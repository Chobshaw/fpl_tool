from dependency_injector import containers, providers
from pymongo import MongoClient

from helpers.mongodb_helper import MongodbHelper
from models.settings_model import Settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    # Gateways
    mongo_client = providers.Singleton(
        MongoClient,
        config.MONGODB_CONNECTION_STRING
    )

    # Databases
    airbnb_collection = providers.Singleton(
        MongodbHelper,
        mongo_client,
        config.AIRBNB_DATABASE,
        config.AIRBNB_COLLECTION
    )
