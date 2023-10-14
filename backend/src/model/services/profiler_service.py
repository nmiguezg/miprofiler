from typing import List, Tuple
from uuid import UUID
import requests
from model.services.To.user_stats import User_stats_to
from model.entities.user import User
from model.entities.collection import Collection
from model.daos.mongo_collection_dao import Mongo_collection_dao
from model.daos.mongo_user_dao import Mongo_user_dao
from model.exceptions import *
from os import environ


class Profiler_service():
    def __init__(self):
        self.url = environ.get("PROFILERS_SERVICE_URL")
        if self.url == None:
            raise RuntimeError("Env var PROFILERS_SERVICE_URL not declared.")
        self.algoritmos = ["modaresi", "grivas"]
        self.collection_dao = Mongo_collection_dao()
        self.user_dao = Mongo_user_dao()

    def profile_collection(self, filename, users_posts, algoritmo: str) -> Collection:
        if algoritmo not in self.algoritmos:
            raise NotSupportedAlgorithmException(algoritmo)

        try:
            response = requests.post(
                self.url+algoritmo, json=users_posts, timeout=1000)

            json = response.json()
            if response.status_code != 200:
                raise ServerNotAvailableException(json)

            users = [User(**user, posts=users_posts[user['user']])
                     for user in json['users']]
            coll = Collection(
                nombre=filename,
                algoritmo=algoritmo,
                tiempo=json['time'],
                users_stats=self.__calculate_user_stats(
                    users)
            )
            coll = self.collection_dao.create(coll)
            self.user_dao.create_collection_users(
                users, coll_id=coll.id)
            return coll

        except requests.exceptions.ConnectionError:
            raise ServerNotAvailableException(
                "The profiling server is not currently avaliable")
        except requests.exceptions.ReadTimeout:
            raise ServerTimeoutException(
                "The profiler took too long profiling the collection, try uploading a smaller one")

    def get_profiled_collection(self, collection_id: UUID) -> Collection:
        return self.collection_dao.get_collection(collection_id)

    def get_collection_users(self, collection_id: UUID, limit, offset, filters) -> Tuple[List[User], bool]:
        self.collection_dao.get_collection(collection_id)
        users, has_more = self.user_dao.get_collection_users(
            collection_id, limit=limit, skip=offset, filters=filters)
        return users, has_more

    def get_collection_stats(self, collection_id: UUID, filters) -> User_stats_to:
        self.collection_dao.get_collection(collection_id)
        filtered_users = self.user_dao.get_filtered_users(
            coll_id=collection_id, filters=filters)
        return User_stats_to(**self.__calculate_user_stats(filtered_users))

    def get_collections_list(self) -> list[Collection]:
        collections = self.collection_dao.get_collections()
        return collections

    def __calculate_user_stats(self, users):
        stats = {
            "total_users": len(users),
            "age": {
                '18-24': 0,
                '25-34': 0,
                '35-49': 0,
                '50-XX': 0
            },
            "gender": {
                "MALE": 0,
                "FEMALE": 0
            }
        }
        for user in users:
            stats['age'][user.age] += 1
            stats['gender'][user.gender] += 1

        return stats
