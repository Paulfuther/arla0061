import json
import time

from flask import jsonify


def stringify_objectid(data):
    str_data = json.dumps(data, default=str)
    return json.loads(str_data)


def response(status, message, data, status_code=200):
    """
    :param status : Boolean Status of the request
    :param status_code: Status Code of response
    :param message : String message to be sent out as description of the message
    :param data : dictionary representing extra data
    """
    if data:
        data = stringify_objectid(data)
    res = {'status': status, 'message': message, 'data': data, 'timestamp': timestamp()}
    return jsonify(res), status_code


def error_response(message, status='error', code='R0', status_code=400):
    res = {'message': message, 'status': status, 'code': code}
    return jsonify(res), status_code


def timestamp():
    """
    Helper Function to generate the current time
    """
    return time.time()