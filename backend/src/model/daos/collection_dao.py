from model.entities.collection import Collection
from abc import ABC, abstractmethod

class Collection_dao(ABC):

    @abstractmethod
    def create(self, collection: Collection):
        pass

    @abstractmethod
    def get_collection(self, id: str):
        pass
    
    @abstractmethod
    def get_collections(self):
        pass

    @abstractmethod
    def update_collection(self, collection: Collection):
        pass

    @abstractmethod
    def remove_collection(self, id: str):
        pass