from datetime import datetime

from dependency_injector.wiring import inject, Provide

from containers.standalone_containers import StandaloneContainer
from services.fixture_data_loader_service import FixtureDataLoaderService
from services.team_rating_service import TeamRatingService


@inject
def main(
        from_timestamp: int,
        to_timestamp: int,
        competitions: list[str],
        data_loader_service: FixtureDataLoaderService = Provide[StandaloneContainer.data_loader_service],
        team_elo_service: TeamRatingService = Provide[StandaloneContainer.team_rating_service]
) -> None:
    # data_loader_service.load_fixture_data_to_mongodb(from_year=2010, to_year=2023, competitions=competitions)
    team_elo_service.get_team_ratings(datetime(2010, 1, 1), datetime(2023, 2, 3))


container = StandaloneContainer()
container.init_resources()
container.wire(modules=[__name__])
event = {
    'from_timestamp': 2010,
    'to_timestamp': 2022,
    'competitions': ['premier_league', 'championship']
}
main(**event)
