from pymongo import MongoClient

from models.mongodb_query_model import MongodbQueryModel


class MongodbHelper:
    def __init__(self, client: MongoClient, database_name: str, collection_name: str) -> None:
        self.database = client[database_name]
        self.collection = self.database[collection_name]

    def query_all_items(self) -> dict:
        return self.collection.find({})[0]

    def query_items_between(self, mongodb_query_model: MongodbQueryModel):
        index_key = mongodb_query_model.index_key
        response = self.collection.find({
            index_key.name: {
                '$gte': index_key.value,
                '$lt': index_key.aux_value
            }
        })
        return {'items': [item for item in response]}

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
