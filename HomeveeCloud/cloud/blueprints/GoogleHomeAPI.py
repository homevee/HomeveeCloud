#!flask/bin/python
import json
import traceback

from flask import Blueprint, abort, request, render_template
from werkzeug.utils import redirect

GoogleHomeAPI = Blueprint('GoogleHomeAPI', __name__, template_folder='templates')

@GoogleHomeAPI.route('/google-home', methods=['GET'])
def handle_google_home_get_query():
    print(request.headers)
    print(request.args)
    data = request.get_json()
    print(data)
    return json.dumps({'status': 'ok'})

@GoogleHomeAPI.route('/google-home', methods=['POST'])
def handle_google_home_post_query():
    print(request.headers)
    print(request.form)
    data = request.get_json()
    print(data)
    return json.dumps({'status': 'ok'})