# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/profile", methods=['POST'])
def profile():
    algoritmo = request.form['algoritmo']
    if algoritmo == 'los_calis':
        pass
    else:
        print(request.files['file'].content_type)
        url = 'http://localhost:5000/profile/'+algoritmo
        files = {'collection': (request.files['file'])}
        response = requests.post(url, files=files)
        print(response.json())
    return response.json(), 200
if __name__ == "__main__":
    app.run(debug=True, port=8000)