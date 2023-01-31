from helpers.mongodb_helper import MongodbHelper
from models.constants_model import Constants


class ParameterStoreHelper:
    def __init__(self, mongodb_helper: MongodbHelper):
        self.mongodb_helper = mongodb_helper
        self.constants = self._get_constants_from_parameter_store()

    def _get_constants_from_parameter_store(self):
        parameter_dict = self.mongodb_helper.query_all_items()
        return Constants.parse_obj(parameter_dict)
