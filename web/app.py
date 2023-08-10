# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
from flask import Flask, render_template, request, jsonify
import requests

from losCalis_profiler import LosCalis_profiler

app = Flask(__name__)
los_calis = LosCalis_profiler()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile", methods=['POST'])
def profile():
    start = time.time()
    algoritmo = request.form['algoritmo']
    if algoritmo == 'los_calis':
        df = los_calis.process_csv(request.files['file'])
        results = los_calis.predict(df)
        return jsonify({'Users': results}), 200
    else:
        print(request.files['file'].content_type)
        url = 'http://localhost:5000/profile/'+algoritmo
        files = {'collection': (request.files['file'])}
        response = requests.post(url, files=files, timeout=10)
    finish = time.time()
    return jsonify(response.json()), 200

if __name__ == "__main__":
    app.run(debug=True, port=8000)