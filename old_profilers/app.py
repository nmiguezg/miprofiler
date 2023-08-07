# -*- coding: utf-8 -*-
#!/usr/bin/env python
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
        # Verificar que se haya enviado un archivo CSV en la solicitud
        if 'collection' not in request.files:
            return jsonify({'error': u'No se proporcionó ningún archivo CSV.'}), 400

        coll = request.files['collection']
        if profiler == 'modaresi':
            prof = moda
        elif profiler == 'grivas':
            prof = grivas
        else:
            return jsonify({'error': u'El profiler seleccionado no es válido'.encode('utf-8')}), 400
        # Leer el contenido del archivo CSV con Pandas
        users, docs = prof.process_csv(coll)
        pred = prof.predict(docs)
        resp = []
        for i, user in enumerate(users):
            r = {
                'user': user,
                'gender': pred[0][i],
                'age': pred[1][i]
                }
            resp.append(r)

        return jsonify({'Users': resp}), 200

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