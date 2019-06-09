#!flask/bin/python
import json
import traceback

from flask import Blueprint, abort, request, render_template
from werkzeug.utils import redirect

OAuthAPI = Blueprint('OAuthAPI', __name__, template_folder='templates')


@OAuthAPI.route('/oauth/', methods=['GET'])
def user_oauth():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    scope = request.args.get('scope')
    state = request.args.get('state')
    response_type = request.args.get('response_type')

    return render_template('oauth_login.html', client_id=client_id, response_type=response_type,
                           scope=scope, redirect_uri=redirect_uri, state=state)


@OAuthAPI.route('/oauth/authorize', methods=['POST'])
def user_oauth_authorize():
    print(request.form)

    client_id = request.form.get('client_id')
    scope = request.form.get('scope')
    redirect_uri = request.form.get('redirect_uri')
    state = request.form.get('state')
    response_type = request.form.get('response_type')
    username = request.form.get('username')
    password = request.form.get('password')
    remote_id = request.form.get('remote_id')

    #TODO verify user on cloud

    is_verified = True

    #temporary test tokens
    auth_code = "dYwb6BYSe59TsdjkUYmbNA8fzW9pFQCvVYRzk5F68KVG8NnXwsfcTLXtpezfrafD"
    access_token = "ZDvjXFzTagZAGUcXhjUyWr6Z9sGmGYWZxutD3dYGYaPY4cZ2GM9ay5yV7ruPFMPb"

    url = redirect_uri + "?state=" + state + "&code=" + auth_code# + '&scope='+scope #+ "&access_token=" + access_token

    data = {
        'scope': scope,
        'oauth_token': auth_code,
        'state': state,
        #'access_token': access_token
    }

    # return json.dumps(data)

    print("redirect url: " + url)

    return url
    #return redirect(url)


@OAuthAPI.route('/oauth/token', methods=['POST'])
def user_oauth_token():
    print(request.form)

    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    state = request.form.get('state')

    redirect_uri = request.form.get('redirect_uri')

    #temporary test tokens
    access_token = "ZDvjXFzTagZAGUcXhjUyWr6Z9sGmGYWZxutD3dYGYaPY4cZ2GM9ay5yV7ruPFMPb"
    refresh_token = "ybqqgCGzMWVKqS2SDVQkSVtVpvkTpNz2Uz2pMLBqN6Kfn9GkfbVCFQMFHf8d9gYq"

    expires_in = 3600
    scope = "Smarthome"


    if redirect_uri is None:
        data = {
            'scope': scope,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'state': state,
            'token_type': 'bearer'
        }
        return json.dumps(data)
    else:
        url = redirect_uri + "?scope=" + scope + "&access_token=" + access_token + "&refresh_token=" \
              + refresh_token + "&expires_in=" + str(expires_in) + "&token_type=bearer"
        print("redirect url: " + url)
        return redirect(url)