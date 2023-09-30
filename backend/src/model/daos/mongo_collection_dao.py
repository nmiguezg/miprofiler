from model.exceptions import InstanceNotFoundException
from model.daos.collection_dao import Collection_dao
from model.daos.mongo_instance import Mongo_instance
from model.entities.collection import Collection
import pymongo
from uuid import uuid4, UUID


class Mongo_collection_dao(Collection_dao):
    def __init__(self):
        db = Mongo_instance.get_instance()
        self.collection = db.create_collection("collection")

    def create(self, collection: Collection) -> Collection:
        try:
            collection.id = uuid4()
            result = self.collection.insert_one({
                "_id": collection.id,
                "nombre": collection.nombre,
                "fecha_creacion": collection.fecha_creacion,
                "algoritmo": collection.algoritmo,
                "estadisticas": collection.users_stats,
                "tiempo": collection.tiempo
            })

            return collection
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)

    def get_collection(self, id: UUID) -> Collection:
        try:
            collection = self.collection.find_one({"_id": id})
            if (collection == None):
                raise InstanceNotFoundException(
                    f"No existe la colección con id: {id}.")

            return Collection(
                id=collection['_id'],
                nombre=collection['nombre'],
                algoritmo=collection['algoritmo'],
                tiempo=collection['tiempo'],
                users_stats=collection['estadisticas'],
            )
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)

    def get_collections(self) -> list[Collection]:
        try:
            collections = self.collection.find({}).sort(
                'fecha_creacion', pymongo.ASCENDING)
            collections = list(collections)

            return list(map(lambda collection: Collection(
                id=collection['_id'],
                nombre=collection['nombre'],
                algoritmo=collection['algoritmo'],
                tiempo=collection['tiempo'],
                users_stats=collection['estadisticas'],
            ), collections))
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)

    def update_collection(self, collection: Collection):
        try:
            self.collection.update_one({"_id": collection.id}, {
                "_id": collection.id,
                "nombre": collection.nombre,
                "fecha_creacion": collection.fecha_creacion,
                "algoritmo": collection.algoritmo,
                "estadisticas": collection.users_stats,
                "tiempo": collection.tiempo
            })
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)

    def remove_collection(self, id: str):
        try:
            self.collection.delete_one({"_id": id})
        except pymongo.errors.PyMongoError as e:
            raise RuntimeError(e)
