from pymongo import MongoClient


class MongodbHelper:
    def __init__(self, client: MongoClient, database_name: str, collection_name: str) -> None:
        self.database = client[database_name]
        self.collection = self.database[collection_name]

    def put_item(self, item: dict) -> None:
        self.collection.insert_one(item)

    def batch_put_items(self, items: list[dict]) -> None:
        self.collection.insert_many(items)

    def batch_put_items_if_not_present(self, items: list[dict], filter_field: str) -> None:
        for item in items:
            self.collection.update_one(
                filter={filter_field: item[filter_field]},
                update={'$setOnInsert': item},
                upsert=True
            )

    def batch_replace_items(self, items: list[dict], filter_field: str) -> None:
        for item in items:
            self.collection.replace_one(
                filter={filter_field: item[filter_field]},
                replacement=item,
                upsert=True
            )
