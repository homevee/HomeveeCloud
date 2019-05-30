#!flask/bin/python
import json
import traceback

from flask import Blueprint, abort, request

from cloud.Helper.Database import Database
from cloud.HomeveeCloud import HomeveeCloud
from cloud.HomeveeServer import HomeveeServer

CloudAPI = Blueprint('CloudAPI', __name__, template_folder='templates')

@CloudAPI.route('/ispremium/<remote_id>', methods=['GET'])
def is_premium(remote_id):
    print("ispremium")
    try:
        assert remote_id == request.view_args['remote_id']
        cloud_url = request.headers['Cloud-URL']
        access_token = request.headers['Server-Secret']
        homevee_cloud = HomeveeCloud(cloud_url)
        is_verified = homevee_cloud.verify_cloud(access_token)

        if not is_verified:
            abort(401)

        homevee_server = HomeveeServer(remote_id)
        return json.dumps({'is_premium': homevee_server.is_premium})
    except:
        traceback.print_exc()
        abort(400)

@CloudAPI.route('/assigncloud/<remote_id>', methods=['PUT'])
def assign_cloud_to_remote_id(remote_id):
    print("ispremium")
    try:
        status = "ok"

        assert remote_id == request.view_args['remote_id']
        cloud_url = request.headers['Cloud-URL']
        server_secret = request.headers['Server-Secret']
        access_token = request.headers['Access-Token']
        homevee_cloud = HomeveeCloud(cloud_url)
        cloud_is_verified = homevee_cloud.verify_cloud(server_secret)

        if not cloud_is_verified:
            abort(401)

        homevee_server = HomeveeServer(remote_id)

        database = Database()
        result = database.do_query("SELECT IS_PREMIUM FROM CLOUDS WHERE CLOUD_URL = %s AND IS_ACTIVE = 1", (cloud_url, ))
        result = result.fetchone()
        print(result)

        if(result is None):
            cloud_is_premium = False
        else:
            cloud_is_premium = True

        if cloud_is_premium and not homevee_server.is_premium:
            status = "nopermission"
        else:
            database.do_query("REPLATE INTO CLOUD_DATA (REMOTE_ID, CLOUD) VALUES (%s, %s", (remote_id, cloud_url,))

        return json.dumps({'status': status, 'verified': homevee_server.verify_server(access_token),
                           'is_premium': homevee_server.is_premium})
    except:
        traceback.print_exc()
        abort(400)