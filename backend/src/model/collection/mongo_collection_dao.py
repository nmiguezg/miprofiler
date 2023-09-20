import configparser
from backend.src.db.create_db import create_bd
from backend.src.model.collection.collection_dao import Collection_dao
from backend.src.model.collection.collection import Collection
from bson.objectid import ObjectId
import configparser
from pymongo import MongoClient

class Mongo_collection_dao(Collection_dao):
    def __init__(self, bd, collection_name):
        config = configparser.ConfigParser()
        config.read("backend/src/resources/configuration_parameters.ini")
        url = f"mongodb://{config['db']['user']}:{config['db']['password']}\
            @{config['db']['host']}:{config['db']['port']}/"
        client = MongoClient(url, maxPoolSize=10)
        create_bd(client, config)
        bd = client[config['db']['name']]
        self.collection = bd[collection_name]

    def create(self, collection: Collection) -> Collection:
        collection.id = self.collection.insert_one({
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "usuarios": collection.users,
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
            users=collection['usuarios'],
        )

    def update_collection(self, collection: Collection):
        self.collection.update_one({
            "_id": collection.id,
            "nombre": collection.nombre,
            "fecha_creacion": collection.fecha_creacion,
            "algoritmo": collection.algoritmo,
            "usuarios": collection.users,
            "tiempo": collection.tiempo
        })

    def remove_collection(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})
