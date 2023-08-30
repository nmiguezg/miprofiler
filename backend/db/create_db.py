import json
from pymongo import MongoClient
import configparser
# config = configparser.ConfigParser()
# config.read('./resources/configuration_parameters.ini')
def create_db(client, config):
    db = client[config['db']['name']]

    # Cargar el JSON Schema desde el archivo
    with open(config['db']['schema']) as schema_file:
        schema = json.load(schema_file)

    result = db.create_collection("miprofiler", validator=schema)