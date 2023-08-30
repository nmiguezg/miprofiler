# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import time
from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import configparser
from pymongo import MongoClient
from 'db/create_db' import create_db
app = Flask(__name__)

config = configparser.ConfigParser()
config.read("./resources/configuration_parameters.ini")
client = MongoClient(f"mongodb://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/", maxPoolSize=10)
create_db(client, config)
bd = client[config['db']['name']]

@app.route("/")
def index():
    return "<h1>Backend</h1>"
@app.route("/profile", methods=['POST'])
@app.route("/profile/", methods=['POST'])
def profile():
    algoritmo = request.form['algoritmo']
    try:
        url = 'http://profilers:5000/profile/'+algoritmo
        files = {'collection': (request.files['file'])}
        response = requests.post(url, files=files, timeout=1000)
        if response.status_code == 200:
            bd['users'].insert_many(process_file(request.files['file'], response))
        return jsonify(response.json()), 200
    except requests.exceptions.ConnectionError:
        return jsonify({'error': "Server isn't available"}), 500
    except requests.exceptions.ReadTimeout:
        return jsonify({'error': "Server is lasting too long \
                        in profiling the dataset, consider divi \
                        ding it in smaller parts"}), 500

def process_file(file, response):
    df = pd.read_csv(file)
    df['post'] = df['post'].transform(lambda x: str(x))
    df = df.groupby(['label'])['post'].apply(list).reset_index()
    df = df.drop_duplicates(subset='label').reset_index(drop=True)
    users = pd.read_json(response.json()['Users'])
    df = pd.merge(df, users, on=['label', 'user'], validate='one_to_one')
    df['date'] = datetime.now().timestamp()
    df['collection'] = file.filename
    return df.iloc[:, :-1].to_dict('records')

@app.route("/users", methods=['GET'])
@app.route("/users/<int:limit><int:offset>", methods=['GET'])
def users(length=100, offset=0):
    users = bd['users'].find({}, {'_id': 0},limit=length, skip=offset)
    return jsonify({'Users': list(users)}), 200
if __name__ == "__main__":
    app.run(debug=False, port=8000, host='0.0.0.0')