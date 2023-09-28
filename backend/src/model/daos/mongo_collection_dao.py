from model.exceptions import InstanceNotFoundException
from model.daos.collection_dao import Collection_dao
from model.daos.mongo_instance import Mongo_instance
from model.entities.collection import Collection
from uuid import uuid4, UUID


class Mongo_collection_dao(Collection_dao):
    def __init__(self):
        db = Mongo_instance.get_instance()
        self.collection = db.create_collection("collection")

    def create(self, collection: Collection) -> Collection:
        collection.id = uuid4()
        self.collection.insert_one({
            "_id": collection.id,
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "estadisticas": collection.users_stats,
            "tiempo": collection.tiempo
        })

        return collection

    def get_collection(self, id: UUID) -> Collection:
        collection = self.collection.find_one({"_id": UUID(id)})
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
    def get_collections(self) -> list[Collection]:
        collections = self.collection.find(options = {"sort":["fecha_creacion", "asc"]})
        return map(lambda collection: Collection(
            id=collection['_id'],
            nombre=collection['nombre'],
            algoritmo=collection['algoritmo'],
            tiempo=collection['tiempo'],
            users_stats=collection['estadisticas'],
        ), collections)
    
    def update_collection(self, collection: Collection):
        self.collection.update_one({"_id": collection.id}, {
            "_id": collection.id,
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "estadisticas": collection.users_stats,
            "tiempo": collection.tiempo
        })

    def remove_collection(self, id: str):
        self.collection.delete_one({"_id": id})
