from typing import Dict
from uuid import UUID
from model.daos.mongo_instance import Mongo_instance
from model.daos.user_dao import User_dao
from model.entities.user import User
import pymongo


class Mongo_user_dao(User_dao):
    def __init__(self):
        db = Mongo_instance.get_instance()
        try:
            self.collection = db.create_collection("user")
        except pymongo.errors.CollectionInvalid as e:
            self.collection = db['user']

    def create_collection_users(self, users: list[User], coll_id: UUID) -> None:
        try:
            self.collection.insert_many([
                {
                    'id': user.id,
                    'age': user.age,
                    'gender': user.gender,
                    'posts': user.posts,
                    'collection_id': coll_id
                } for user in users
            ])
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)

    def get_collection_users(self, coll_id: UUID, filters,
                             limit: int = 0, skip: int = 0) -> list[User]:
        try:
            filters = {**filters, "collection_id": coll_id}
            users = self.collection.find(filters, {
                "_id": False, "collection_id": False},
                skip=skip, limit=limit).sort("id", pymongo.ASCENDING)

            return [
                User(
                    id=user['id'],
                    age=user['age'],
                    gender=user['gender'],
                    posts=user['posts'],
                    collection_id=coll_id
                ) for user in users
            ]
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)

    def get_filtered_users(self, coll_id: UUID, filters: Dict[str, str | UUID]) -> list[User]:
        try:
            filters = {**filters, "collection_id": coll_id}
            users = self.collection.find(filters, {
                "_id": False, "collection_id": False, "posts": False})

            return [
                User(
                    id=user['id'],
                    age=user['age'],
                    gender=user['gender']
                ) for user in users
            ]
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)
