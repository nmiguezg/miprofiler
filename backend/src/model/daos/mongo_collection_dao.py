from model.exceptions import InstanceNotFoundException
from model.daos.collection_dao import Collection_dao
from model.daos.mongo_instance import Mongo_instance
from model.entities.collection import Collection
from bson.objectid import ObjectId

class Mongo_collection_dao(Collection_dao):
    def __init__(self):
        db = Mongo_instance.get_instance()
        self.collection = db.create_collection("collection")

    def create(self, collection: Collection) -> Collection:
        binary_id = self.collection.insert_one({
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "estadisticas": collection.users_stats,
            "tiempo": collection.tiempo
        }).inserted_id
        collection.id = (binary_id)

        return collection

    def get_coleccion(self, id: str) -> Collection:
        collection = self.collection.find_one({"_id": ObjectId(id)})
        if (collection == None):
            raise InstanceNotFoundException(f"No existe la colección con id: {id}.")
        
        return Collection(
            id=collection['_id'],
            nombre=collection['nombre'],
            algoritmo=collection['algoritmo'],
            tiempo=collection['tiempo'],
            users_stats=collection['estadisticas'],
        )

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
        self.collection.delete_one({"_id": ObjectId(id)})
