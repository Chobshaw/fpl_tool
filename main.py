from dependency_injector.wiring import inject, Provide

from containers.standalone_containers import StandaloneContainer
from services.fixture_data_loader_service import FixtureDataLoaderService


@inject
def main(
        from_timestamp: int,
        to_timestamp: int,
        competitions: list[str],
        data_loader_service: FixtureDataLoaderService = Provide[StandaloneContainer.data_loader_service]
) -> None:
    data_loader_service.load_historical_fixture_data_to_mongodb(from_year=2010, to_year=2023, competitions=competitions)


container = StandaloneContainer()
container.init_resources()
container.wire(modules=[__name__])
event = {
    'from_timestamp': 2010,
    'to_timestamp': 2022,
    'competitions': ['premier_league', 'championship']
}
main(**event)
