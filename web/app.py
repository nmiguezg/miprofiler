# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/profile", methods=['POST'])
@app.route("/profile/", methods=['POST'])
def profile():
    start = time.time()
    algoritmo = request.form['algoritmo']
    try:
        url = 'http://localhost:5000/profile/'+algoritmo
        files = {'collection': (request.files['file'])}
        response = requests.post(url, files=files, timeout=(3.05, 45))
        if response.status_code != 200:
            print(response.json())
        finish = time.time()
        return jsonify(response.json()), 200
    except requests.exceptions.ConnectionError:
        return jsonify({'error': "Server isn't available"}), 500
    except requests.exceptions.ReadTimeout:
        return jsonify({'error': "Server is lasting too long \
                        in profiling the dataset, consider divi \
                        ding it in smaller parts"}), 500


if __name__ == "__main__":
    app.run(debug=False, port=8000)