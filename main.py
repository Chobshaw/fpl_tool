from dependency_injector.wiring import Provide, inject

from containers.containers import Container
from helpers.mongodb_helper import MongodbHelper


@inject
def main(airbnb_collection: MongodbHelper = Provide[Container.airbnb_collection]):
    for val in airbnb_collection.collection.find({'property_type': 'House'})[:3]:
        print(val)


container = Container()
container.init_resources()
container.wire(modules=[__name__])
main()
