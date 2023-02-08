from dependency_injector import containers, providers
from pymongo import MongoClient

from helpers.mongodb_helper import MongodbHelper
from helpers.parameter_store_helper import ParameterStoreHelper
from models.settings_model import StandaloneSettings
from rating_systems.rating_models import EloModel
from services.fixture_data_loader_service import FixtureDataLoaderService
from services.team_rating_service import TeamRatingService


class StandaloneContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[StandaloneSettings()])

    # Gateways
    mongo_client = providers.Singleton(
        MongoClient,
        config.MONGODB_CONNECTION_STRING
    )

    # Collections
    parameter_store_collection = providers.Singleton(
        MongodbHelper,
        client=mongo_client,
        database_name=config.PARAMETER_STORE_DATABASE_NAME,
        collection_name=config.PARAMETERS_COLLECTION_NAME
    )

    fixtures_collection = providers.Singleton(
        MongodbHelper,
        client=mongo_client,
        database_name=config.TEAM_DATA_DATABASE_NAME,
        collection_name=config.FIXTURES_COLLECTION_NAME
    )

    team_instances_collection = providers.Singleton(
        MongodbHelper,
        client=mongo_client,
        database_name=config.TEAM_DATA_DATABASE_NAME,
        collection_name=config.TEAM_INSTANCES_COLLECTION_NAME
    )

    # Parameter store
    parameter_store_helper = providers.Singleton(
        ParameterStoreHelper,
        mongodb_helper=parameter_store_collection
    )

    # Tools
    elo_model = providers.Factory(
        EloModel
    )

    # Services
    data_loader_service = providers.Factory(
        FixtureDataLoaderService,
        fixtures_collection=fixtures_collection,
        constants=parameter_store_helper.provided.constants.fixture_data_loader_constants
    )

    team_rating_service = providers.Factory(
        TeamRatingService,
        fixtures_collection=fixtures_collection,
        team_instances_collection=team_instances_collection,
        constants=parameter_store_helper.provided.constants.team_rating_service_constants,
        rater=elo_model
    )
