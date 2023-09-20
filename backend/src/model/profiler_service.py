import pandas as pd
import requests
from backend.src.model.collection.collection import Collection
from backend.src.model.collection.mongo_collection_dao import Mongo_collection_dao

from backend.src.model.exceptions import *


class Profiler_service():
    def __init__(self):
        self.url = 'http://profilers:5000/profile/'
        self.algoritmos = ["modaresi", "grivas"]
        self.collection_dao = Mongo_collection_dao()

    def profile_collection(self, algoritmo: str, file):
        if algoritmo not in self.algoritmos:
            raise NotSupportedAlgorithmException(algoritmo)

        files = {'collection': file}
        try:
            response = requests.post(
                self.url+algoritmo, files=files, timeout=1000)
            if response.status_code != 200:
                raise Exception(response.json)
            coll = Collection(
                nombre=file.name,
                algoritmo=algoritmo,
                tiempo=response.json['time'],
                users=response.json['users'],
            )
            coll.id = self.collection_dao.create(coll)
            return coll

        except requests.exceptions.ConnectionError:
            raise ServerNotAvailableException()
        except requests.exceptions.ReadTimeout:
            raise ServerTimeoutException()
        except:
            raise RuntimeError(
                "Error inserting the collection in the database")
