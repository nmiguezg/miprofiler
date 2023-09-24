from model.daos.mongo_instance import Mongo_instance
from model.daos.user_dao import User_dao
from model.entities.user import User


class Mongo_user_dao(User_dao):
    def __init__(self):
        db = Mongo_instance.get_instance()
        self.collection = db.create_collection("user")

    def create_collection_users(self, users: list[dict], coll_id: str) -> None:
        self.collection.insert_many([
            {
                'id': user['user'],
                'age': user['age'],
                'gender': user['gender'],
                'posts': user['posts'],
                'collection_id': coll_id
            } for user in users
        ])

    def get_collection_users(self, coll_id: str, limit: int = 0, skip: int = 0) -> list[User]:
        users = self.collection.find({"collection_id": coll_id}, {
                                     "_id": False, "collection_id": False},
                                     skip=skip, limit=limit)
        return [
            User(
                id=user.id,
                age=user.age,
                gender=user.gender,
                posts=user.posts,
                collection_id=coll_id
            ) for user in users
        ]
