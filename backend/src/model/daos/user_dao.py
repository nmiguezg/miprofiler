from uuid import UUID
from model.entities.collection import Collection
from abc import ABC, abstractmethod

from model.entities.user import User


class User_dao(ABC):

    @abstractmethod
    def create_collection_users(self, users: list[User | dict], coll_id: UUID):
        pass

    @abstractmethod
    def get_collection_users(self, id_coll: str, skip: int, limit: int):
        pass