#!flask/bin/python
import json
import traceback

from flask import Blueprint, abort, request, render_template
from werkzeug.utils import redirect

AlexaAPI = Blueprint('AlexaAPI', __name__, template_folder='templates')

@AlexaAPI.route('/alexa', methods=['GET'])
def handle_alexa_get_query():
    print(request.headers)
    print(request.args)
    data = request.get_json()
    print(data)
    return json.dumps({'status': 'ok'})

@AlexaAPI.route('/alexa', methods=['POST'])
def handle_alexa_post_query():
    print(request.headers)
    print(request.form)
    data = request.get_json()
    print(data)
    return json.dumps({'status': 'ok'})