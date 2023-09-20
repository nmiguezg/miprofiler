import json

def create_bd(client, config):
    # Eliminar la base de datos si existe
    if config['db']['name'] in client.list_database_names():
        client.drop_database(config['db']['name'])

    db = client[config['db']['name']]

    # Cargar el JSON Schema desde el archivo
    with open(config['db']['schema']) as schema_file:
        schema = json.load(schema_file)

    result = db.create_collection("miprofiler", validator=schema)