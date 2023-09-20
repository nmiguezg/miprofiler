from backend.src.model.collection import Collection
from abc import ABC, abstractmethod
from bson.objectid import ObjectId

from backend.src.model.user import User


class Collection_dao(ABC):

    @abstractmethod
    def create(self, collection: Collection):
        pass

    @abstractmethod
    def get_coleccion(self, id: str):
        pass

    @abstractmethod
    def update_collection(self, collection: Collection):
        pass

    @abstractmethod
    def remove_collection(self, id: str):
        pass


class Mongo_collection_dao(Collection_dao):
    def __init__(self, bd, collection_name):
        self.collection = bd[collection_name]

    def create(self, collection: Collection) -> Collection:
        collection.id = self.collection.insert_one({
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "usuarios": map(self.__user_to_dict, collection.users),
            "tiempo": collection.tiempo
        })
        return collection

    def get_coleccion(self, id: str) -> Collection:
        collection = self.collection.find_one({"_id": ObjectId(id)})
        return Collection(
            id=collection['_id'],
            nombre=collection['nombre'],
            algoritmo=collection['algoritmo'],
            tiempo=collection['tiempo'],
            users=map(self.__dict_to_user, collection['usuarios']),
        )

    def update_collection(self, collection: Collection):
        self.collection.update_one({
            "_id": collection.id,
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "usuarios": map(self.__user_to_dict, collection.users),
            "tiempo": collection.tiempo
        })

    def remove_collection(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})

    def __user_to_dict(user) -> dict:
        return {
            "id": user.id,
            "posts": user.posts,
            "gender": user.gender,
            "age": user.age,
        }

    def __dict_to_user(user) -> User:
        return User(
            user['id'],
            user['posts'],
            user['gender'],
            user['age']
        )
