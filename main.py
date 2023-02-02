from datetime import datetime

from dependency_injector.wiring import inject, Provide

from containers.standalone_containers import StandaloneContainer
from services.fixture_data_loader_service import FixtureDataLoaderService
from services.team_elo_service import TeamEloService


@inject
def main(
        from_timestamp: int,
        to_timestamp: int,
        competitions: list[str],
        data_loader_service: FixtureDataLoaderService = Provide[StandaloneContainer.data_loader_service],
        team_elo_service: TeamEloService = Provide[StandaloneContainer.team_elo_service]
) -> None:
    # data_loader_service.load_historical_fixture_data_to_mongodb(from_year=2010, to_year=2023, competitions=competitions)
    team_elo_service.calculate_elo_data(datetime(2010, 1, 1), datetime(2011, 1, 1))


container = StandaloneContainer()
container.init_resources()
container.wire(modules=[__name__])
event = {
    'from_timestamp': 2010,
    'to_timestamp': 2022,
    'competitions': ['premier_league', 'championship']
}
main(**event)
