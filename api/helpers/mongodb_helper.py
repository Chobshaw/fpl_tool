from pymongo import MongoClient

client = MongoClient('localhost', 27017)


class MongodbHelper:
    def __init__(self, database_name: str, collection_name: str) -> None:
        self.database = client[database_name]
        self.collection = self.database[collection_name]
