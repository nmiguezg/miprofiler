# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import traceback
from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import configparser
from pymongo import MongoClient
from db.create_db import create_db
import copy


app = Flask(__name__)

config = configparser.ConfigParser()
config.read("./resources/configuration_parameters.ini")
client = MongoClient(f"mongodb://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/", maxPoolSize=10)
create_db(client, config)
print("Database created", flush=True)
bd = client[config['db']['name']]

@app.route("/")
def index():
    return "<h1>Backend</h1>"
@app.route("/profile", methods=['POST'])
def profile():
    try:
        
        url = 'http://profilers:5000/profile/' + request.form.get('algoritmo')
        file = request.files['file']
        files = {'collection': file}
        response = requests.post(url, files=files, timeout=1000)
        if response.status_code == 200:
            file.seek(0)
            resp = process_file(file, response)
            copy_resp = copy.deepcopy(resp)
            bd['users'].insert_many(copy_resp)
        return jsonify(resp), 200
    except requests.exceptions.ConnectionError:
        return jsonify({'error': "Server isn't available"}), 500
    except requests.exceptions.ReadTimeout:
        return jsonify({'error': "Server is lasting too long \
                        in profiling the dataset, consider divi \
                        ding it in smaller parts"}), 500
    except Exception as e:
        return jsonify({'error': str(traceback.format_exc())}), 500
    

def process_file(file, response):
    df = pd.read_csv(file, encoding='utf-8')
    df['post'] = df['post'].transform(lambda x: str(x))
    df = df.groupby(['label'])['post'].apply(list).reset_index()
    df = df.drop_duplicates(subset='label').reset_index(drop=True)
    users = pd.DataFrame(response.json()['Users'])
    df = pd.merge(df, users, left_on='label', right_on='user', validate='one_to_one')
    df['date'] = datetime.datetime.now().timestamp()
    df['collection'] = file.filename
    df = df[['age', 'gender', 'collection', 'label', 'post', 'date']]
    return df.to_dict('records')

@app.route("/users", methods=['GET'])
@app.route("/users/", methods=['GET'])
def users(limit=100, offset=0):
    if request.args.get('limit')!=None:
        limit = int(request.args.get('limit'))
    if request.args.get('offset')!=None:
        offset = int(request.args.get('offset'))

    users = bd['users'].find({}, {'_id': 0},limit=limit, skip=offset)
    return jsonify({'Users': list(users)}), 200
if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)