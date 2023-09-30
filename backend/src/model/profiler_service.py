from uuid import UUID
import requests
from model.entities.user import User
from model.entities.collection import Collection
from model.daos.mongo_collection_dao import Mongo_collection_dao
from model.daos.mongo_user_dao import Mongo_user_dao
from model.exceptions import *
from os import environ


class Profiler_service():
    def __init__(self):
        self.url = environ.get("PROFILERS_SERVICE_URL")
        self.algoritmos = ["modaresi", "grivas"]
        self.collection_dao = Mongo_collection_dao()
        self.user_dao = Mongo_user_dao()

    def profile_collection(self, file, algoritmo: str) -> Collection:
        if algoritmo not in self.algoritmos:
            raise NotSupportedAlgorithmException(algoritmo)

        files = {'collection': file}
        self.__validate_file(file=file)
        try:
            response = requests.post(
                self.url+algoritmo, files=files, timeout=1000)

            json = response.json()

            if response.status_code != 200:
                raise ServerNotAvailableException(json)

            coll = Collection(
                nombre=file.filename,
                algoritmo=algoritmo,
                tiempo=json['time'],
                users_stats=self.__calculate_user_stats(
                    json['users'])
            )
            coll = self.collection_dao.create(coll)
            self.user_dao.create_collection_users(
                json['users'], coll_id=coll.id)
            return coll

        except requests.exceptions.ConnectionError:
            raise ServerNotAvailableException(
                "The profiling server is not currently avaliable")
        except requests.exceptions.ReadTimeout:
            raise ServerTimeoutException(
                "The profiler took too long profiling the collection, try uploading a smaller one")

    def get_profiled_collection(self, collection_id: UUID) -> Collection:
        return self.collection_dao.get_collection(collection_id)

    def get_collection_users(self, id, limit, offset) -> list[User]:
        self.collection_dao.get_collection(id)
        users = self.user_dao.get_collection_users(
            id, limit=limit, skip=offset)
        return users

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
            gender = "MALE" if user['gender'][0] == 'M' else "FEMALE"
            stats['age'][user['age']] += 1
            stats['gender'][gender] += 1

        return stats

    def __validate_file(self, file):
        if file == None:
            raise InvalidFileException(
                "No se ha subido ningún archivo para ser perfilado")
        if not file.filename.endswith(".csv"):
            raise InvalidFileException(
                "El archivo subido no tiene el formato adecuado")
        # try:
        #     lector_csv = csv.reader(file)

        #     columns = next(lector_csv)

        #     # Verificar que las columnas "id" y "posts" estén presentes
        #     if not {"id", "posts"} <= set(columns):
        #         raise InvalidFileException(
        #             "El archivo debe contener al menos las siguientes columnas {id, posts}")
        # except Exception as e:
        #     raise RuntimeError(e.args)
