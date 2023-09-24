# -*- coding: utf-8 -*-
#!/usr/bin/env python
import traceback
from flask import Flask, request, jsonify
from model.exceptions import InstanceNotFoundException, ServerNotAvailableException
from model.exceptions import ServerTimeoutException
from model.exceptions import InvalidFileException
from model.profiler_service import Profiler_service

app = Flask(__name__)
profiler_service = Profiler_service()


@app.route("/")
def index():
    return "<h1>Backend</h1>"


@app.route("/profile", methods=['POST'])
def profile():
    try:
        coll = profiler_service.profile_collection(
            algoritmo=request.form.get('algoritmo'),
            file=request.files['file']
        )
        return coll.__dict__, 201
    except ServerNotAvailableException:
        return jsonify({'error': "Profiling server isn't available"}), 500
    except ServerTimeoutException:
        return jsonify({'error': "Profiling server is lasting too long \
                        in profiling the dataset, consider divi \
                        ding it in smaller parts"}), 500
    except InvalidFileException as e:
        return jsonify({'error': e.msg}), 400
    except Exception as e:
        return jsonify({'error': traceback.format_exc()}), 500


@app.route("/users", methods=['GET'])
@app.route("/users/", methods=['GET'])
def users(limit=0, offset=0):
    if request.args.get('coll_id') == None:
        return jsonify({"Error": "Collection identifier not specified."}), 400
    
    coll_id = request.args.get('coll_id')
    limit = request.args.get('limit')
    if  limit!= None:
        limit = int(limit)
    offset = request.args.get('offset')
    if offset != None:
        offset = int(offset)
    
    try:

        users = profiler_service.get_collection_users(
            id=coll_id, limit=limit, offset=offset
        )
        dict_users = [user.__dict__ for user in users]
        return jsonify({'Users': dict_users}), 200
    except InstanceNotFoundException as e:
        return jsonify({"error": e.msg}), 404
    except RuntimeError as e:
        return jsonify({'error': traceback.format_exc()}), 500



if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
