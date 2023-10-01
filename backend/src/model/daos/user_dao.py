from typing import Dict
from uuid import UUID
from model.entities.collection import Collection
from abc import ABC, abstractmethod

from model.entities.user import User


class User_dao(ABC):

    @abstractmethod
    def create_collection_users(self, users: list[User | dict], coll_id: UUID):
        pass

    @abstractmethod
    def get_collection_users(self, coll_id: str, filters: Dict[str, Dict],
                             limit: int = 0, skip: int = 0) -> list[User]:
        pass

    def get_filtered_users(self, coll_id: str, filters: Dict[str, Dict]) -> list[User]:
        pass
