import json
from pymongo import MongoClient
import configparser
# config = configparser.ConfigParser()
# config.read('./resources/configuration_parameters.ini')
def create_db(client, config):
    # Eliminar la base de datos si existe
    if config['db']['name'] in client.list_database_names():
        client.drop_database(config['db']['name'])
        print(f"Database {config['db']['name']} dropped", flush=True)
    else:
        print(f"Database {config['db']['name']} doesn't exist", flush=True)

    db = client[config['db']['name']]

    # Cargar el JSON Schema desde el archivo
    with open(config['db']['schema']) as schema_file:
        schema = json.load(schema_file)

    result = db.create_collection("miprofiler", validator=schema)