from typing import Any

from pymongo import MongoClient

from models.mongodb_query_model import MongodbQueryModel


class MongodbHelper:
    def __init__(self, client: MongoClient, database_name: str, collection_name: str) -> None:
        self.database = client[database_name]
        self.collection = self.database[collection_name]

    def query_all_items(self) -> dict[Any, Any]:
        return self.collection.find({})[0]

    def query_items_between(self, mongodb_query_model: MongodbQueryModel) -> dict[str, Any]:
        sort_key = mongodb_query_model.sort_key
        response = self.collection.find({
            sort_key.name: {
                '$gte': sort_key.value,
                '$lt': sort_key.aux_value
            }
        })
        return {'items': [item for item in response]}

    def query_most_recent_item(self, mongodb_query_model: MongodbQueryModel) -> Any:
        partition_key, sort_key = mongodb_query_model.partition_key, mongodb_query_model.sort_key
        response = self.collection.find({
            partition_key.name: partition_key.value,
            sort_key.name: {'$lte': sort_key.value}
        }).sort({sort_key.name: -1}).limit(1)
        return response[0]

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

    def batch_update_items(self, items: list[dict], filter_field: str, update_field: str) -> None:
        for item in items:
            self.collection.update_one(
                filter={filter_field: item[filter_field]},
                update={'$set': {update_field: item[update_field]}},
                upsert=True
            )

    def batch_replace_items(self, items: list[dict], filter_field: str) -> None:
        for item in items:
            self.collection.replace_one(
                filter={filter_field: item[filter_field]},
                replacement=item,
                upsert=True
            )

    def delete_all_items(self) -> None:
        self.collection.delete_many(
            filter={}
        )
