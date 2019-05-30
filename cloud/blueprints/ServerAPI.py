#!flask/bin/python
import json
import traceback

from flask import Blueprint, abort, request

from cloud.Helper.Database import Database
from cloud.Helper.FirebaseAPI import FirebaseAPI
from cloud.HomeveeServer import HomeveeServer
from cloud.Helper.Utils import Utils

ServerAPI = Blueprint('SeverAPI', __name__, template_folder='templates')

@ServerAPI.route('/ispremium/<remote_id>', methods=['GET'])
def is_premium(remote_id):
    print("ispremium")
    try:
        assert remote_id == request.view_args['remote_id']
        access_token = request.headers['Access-Token']
        homevee_server = HomeveeServer(remote_id)
        is_verified = homevee_server.verify_server(access_token)
        if not is_verified:
            abort(401)
        return json.dumps({'is_premium': homevee_server.is_premium})
    except:
        traceback.print_exc()
        abort(400)\

@ServerAPI.route('/premiumuntil/<remote_id>', methods=['GET'])
def is_premium_until(remote_id):
    print("ispremiumuntil")
    try:
        assert remote_id == request.view_args['remote_id']
        access_token = request.headers['Access-Token']
        homevee_server = HomeveeServer(remote_id)
        is_verified = homevee_server.verify_server(access_token)
        if not is_verified:
            abort(401)
        return json.dumps({'is_premium': homevee_server.is_premium,
                           'premium_until': homevee_server.premium_until})
    except:
        traceback.print_exc()
        abort(400)

@ServerAPI.route('/setlocalip/<remote_id>', methods=['PUT'])
def set_local_ip(remote_id):
    print("ispremium")
    try:
        assert remote_id == request.view_args['remote_id']
        access_token = request.headers['Access-Token']
        homevee_server = HomeveeServer(remote_id)
        is_verified = homevee_server.verify_server(access_token)
        if not is_verified:
            abort(401)

        data = request.get_json()
        ip = data['ip']
        homevee_server.update_ip(ip)

        return json.dumps({'status': 'ok'})
    except:
        traceback.print_exc()
        abort(400)

@ServerAPI.route('/setlocalcert/<remote_id>', methods=['PUT'])
def set_local_cert(remote_id):
    print("ispremium")
    try:
        assert remote_id == request.view_args['remote_id']
        access_token = request.headers['Access-Token']
        homevee_server = HomeveeServer(remote_id)
        is_verified = homevee_server.verify_server(access_token)
        if not is_verified:
            abort(401)

        data = request.get_json()
        cert_data = data['cert']
        homevee_server.update_cert(cert_data)

        return json.dumps({'status': 'ok'})
    except:
        traceback.print_exc()
        abort(400)

@ServerAPI.route('/getcloudtouse/<remote_id>', methods=['GET'])
def get_cloud_to_use(remote_id):
    print("ispremium")
    try:
        assert remote_id == request.view_args['remote_id']
        access_token = request.headers['Access-Token']

        homevee_server = HomeveeServer(remote_id)
        is_verified = homevee_server.verify_server(access_token)
        if not is_verified:
            abort(401)

        database = Database()

        #sql = """SELECT SERVER_DATA.REMOTE_ID, CLOUD_IP, (SELECT COUNT(*) FROM CLOUD_DATA WHERE CLOUD_IP = CLOUD_IP)
        #    as USERS, MAX_USERS FROM CLOUDS, SERVER_DATA WHERE SERVER_DATA.REMOTE_ID = %s AND CLOUDS.IS_ACTIVE = 1
        #    ORDER BY (USERS/MAX_USERS)/IF(CLOUDS.IS_PREMIUM = SERVER_DATA.IS_PREMIUM, 100, 1) ASC LIMIT 1;"""

        sql = """SELECT SERVER_DATA.REMOTE_ID, CLOUD_IP, (SELECT COUNT(*) FROM CLOUD_DATA WHERE CLOUD_IP = CLOUD_IP) 
            as USERS, MAX_USERS FROM CLOUDS, SERVER_DATA WHERE SERVER_DATA.REMOTE_ID = %s AND CLOUDS.IS_ACTIVE = 1
            ORDER BY (USERS/MAX_USERS)/IF(CLOUDS.IS_PREMIUM = SERVER_DATA.IS_PREMIUM, 100, 1) ASC LIMIT 1;"""

        result = database.do_query(sql, (remote_id,))

        remote_id, cloud_ip, users, max_users = result.fetchone()

        return json.dumps({'cloud': cloud_ip})
    except:
        traceback.print_exc()
        abort(400)

@ServerAPI.route('/sendnotification', methods=['POST'])
def send_notification():
    print("ispremium")
    try:
        remote_id = request.headers['Remote-ID']
        access_token = request.headers['Access-Token']
        homevee_server = HomeveeServer(remote_id)
        is_verified = homevee_server.verify_server(access_token)
        if not is_verified:
            abort(401)

        data = request.get_json()
        registration_ids = data['registration_ids']
        message_data = data['message_data']

        FirebaseAPI.send_notification(registration_ids, message_data)

        return json.dumps({'status': 'ok'})
    except:
        traceback.print_exc()
        abort(400)