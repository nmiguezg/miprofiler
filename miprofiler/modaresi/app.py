# -*- coding: utf-8 -*-
#!/usr/bin/env python
import flask
from flask import request, jsonify

from profilers import Modaresi_profiler
import traceback


app = flask.Flask(__name__)
# app.debug = True  # Activa el modo de depuración
# app.config["DEBUG"] = True

moda = Modaresi_profiler()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/profile', methods=['POST'])
def profile():
    try:
        # Verificar que se haya enviado un archivo CSV en la solicitud
        if 'collection' not in request.files:
            return jsonify({'error': 'No se proporcionó ningún archivo CSV.'.encode('utf-8')}), 400

        coll = request.files['collection']

        # Leer el contenido del archivo CSV con Pandas
        users, docs = moda.process_csv(coll)
        pred = moda.predict(docs)
        resp = []
        for user, i in enumerate(users):
            r = {
                'user': user,
                'gender': pred[0][i],
                'age': pred[1][i]
                }
            resp.append(r)
        # Realizar operaciones adicionales con el DataFrame si es necesario
        # Por ejemplo, puedes procesar los datos, realizar análisis o guardarlos en una base de datos.

        return flask.jsonify({'Users': resp}), 200

    except Exception as e:
        return jsonify({'error': (u"Ocurrió un error al cargar el archivo CSV."+(traceback.format_exc()))}), 500


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)