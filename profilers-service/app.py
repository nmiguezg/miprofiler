# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
import flask
from flask import request, jsonify

from profilers import Grivas_profiler, Modaresi_profiler
import traceback

app = flask.Flask(__name__)
moda = Modaresi_profiler()
grivas = Grivas_profiler()


@app.route("/")
def hello_world():
    return "<p>Backend profiler: modaresi and grivas</p>"


@app.route('/profile', methods=['POST'])
@app.route('/profile/<string:profiler>', methods=['POST'])
def profile(profiler='modaresi'):
    try:
        user_posts = request.get_json()

        if profiler == 'modaresi':
            prof = moda
        elif profiler == 'grivas':
            prof = grivas
        else:
            return jsonify({'error': u'El profiler seleccionado no es válido'.encode('utf-8')}), 400
        start = time.time()
        users = user_posts.keys()
        docs = prof.join_posts(user_posts.values())

        pred = prof.predict(docs)
        finish = time.time()
        resp = []
        for i, user in enumerate(users):
            r = {
                'user': int(user),
                'gender': pred[0][i],
                'age': pred[1][i]
            }
            resp.append(r)
        profiling_time = finish-start
        return jsonify({'users': resp, "time": profiling_time}), 200

    except Exception as e:
        return jsonify({'error': (u"Ocurrió un error al cargar el archivo CSV."+(traceback.format_exc()))}), 500


@app.route('/profile/text', methods=['POST'])
@app.route('/profile/text/<string:profiler>', methods=['POST'])
def profile_text(profiler='modaresi'):
    if profiler == 'modaresi':
        prof = moda
    elif profiler == 'grivas':
        prof = grivas
    else:
        return jsonify({'error': u'El profiler seleccionado no es válido'.encode('utf-8')}), 400
    pred = prof.predict([request.data])
    r = {
        'gender': pred[0][0],
        'age': pred[1][0]
    }
    return jsonify({'User': r})
