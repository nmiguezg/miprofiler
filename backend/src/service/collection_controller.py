# -*- coding: utf-8 -*-
#!/usr/bin/env python
import traceback
from service.dtos.Users_filters_dto import validate_filters
from flask import Flask, request, jsonify
from model.exceptions import InputValidationException
from model.exceptions import InstanceNotFoundException, ServerNotAvailableException
from model.exceptions import ServerTimeoutException, NotSupportedAlgorithmException
from model.exceptions import InvalidFileException
from model.services.profiler_service import Profiler_service

app = Flask(__name__)
profiler_service = Profiler_service()


@app.route("/")
def index():
    return "<h1>Backend</h1>"


@app.route("/profiler/profile", methods=['POST'])
def profile():
    try:
        coll = profiler_service.profile_collection(
            algoritmo=__get_mandatory_parameter(request, 'algoritmo', False),
            file=__get_mandatory_file(request, 'file')
        )
        return coll.__dict__, 201
    except (ServerTimeoutException, ServerNotAvailableException) as e:
        return e.json(), 500
    except (InvalidFileException, NotSupportedAlgorithmException, InputValidationException) as e:
        return e.json(), 400


@app.route("/profiler/collections/<uuid:collection_id>", methods=['GET'])
def get_collection(collection_id):
    try:

        coll = profiler_service.get_profiled_collection(collection_id)
        return coll.__dict__, 200
    except InstanceNotFoundException as e:
        return e.json(), 404


@app.route("/profiler/collections", methods=['GET'])
def get_collections():
    try:
        coll = profiler_service.get_collections_list()
        list_dicts = [doc.__dict__ for doc in coll]
        return list_dicts, 200
    except InstanceNotFoundException as e:
        return e.json(), 404


@app.route("/profiler/collections/<uuid:collection_id>/users", methods=['GET'])
def get_collection_users(collection_id):
    limit = __get_optional_int_parameter(request, "limit")
    offset = __get_optional_int_parameter(request, "offset")
    filters = validate_filters(request.args)

    try:
        users = profiler_service.get_collection_users(
            id=collection_id, limit=limit, offset=offset, filters=filters
        )
        list_dicts = [user.__dict__ for user in users]
        return list_dicts, 200
    except InstanceNotFoundException as e:
        return e.json(), 404


@app.route("/profiler/collections/<uuid:collection_id>/stats", methods=['GET'])
def get_collection_stats(collection_id):
    filters = validate_filters(request.args)

    try:
        stats = profiler_service.get_collection_stats(
            collection_id==collection_id, filters=filters
        )
        return stats, 200
    except InstanceNotFoundException as e:
        return e.json(), 404


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': {
        'errorType': "InvalidPath",
        "message": "Invalid path. The requested resource doesn't exist"}}), 404


@app.errorhandler(RuntimeError)
def runtime_exception_handler(exception):
    return jsonify({"error": {
        'errorType': "RuntimeError",
        "traceback": traceback.format_exc()}
    }), 500


def __get_mandatory_parameter(request, param_name, path=True):
    if path:
        param_value = request.args.get(param_name)
    else:
        param_value = request.form.get(param_name)

    if param_value is None:
        raise InputValidationException(
            f"Invalid Request: parameter {param_name} is mandatory")
    return param_value


def __get_optional_int_parameter(request, param_name, default_value=0):
    param_value = request.args.get(param_name)
    if param_value is None:
        param_value = default_value
    return int(param_value)


def __get_mandatory_file(request, param_name):
    param_value = request.files[param_name]
    if param_value is None:
        raise InputValidationException(
            f"Invalid Request: file {param_name} is mandatory")
    return param_value


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
