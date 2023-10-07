import configparser
from pymongo import MongoClient


class Mongo_instance():
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance != None:
            return cls.instance

        config = configparser.ConfigParser()
        config.read("resources/configuration_parameters.ini")

        url = f"mongodb://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/"
        client = MongoClient(url, maxPoolSize=10, uuidRepresentation='standard')

        # Eliminar la base de datos si existe
        # if config['db']['name'] in client.list_database_names():
        #         client.drop_database(config['db']['name'])
                
        cls.instance = client[config['db']['name']]

        return cls.instance