#!flask/bin/python
import json
import traceback

from flask import Blueprint, abort, request

from cloud.CloudNode_Azure import CloudNode
from cloud.HomeveeCloud import HomeveeCloud
from cloud.HomeveeServer import HomeveeServer
from cloud.Helper.Utils import Utils

PublicAPI = Blueprint('PublicAPI', __name__, template_folder='templates')

@PublicAPI.route('/getlocalip/<remote_id>', methods=['GET'])
def get_local_ip(remote_id):
    print("get_local_ip")
    try:
        assert remote_id == request.view_args['remote_id']
        homevee_server = HomeveeServer(remote_id)
        
        return json.dumps({'local_ip': homevee_server.get_ip()})
    except:
        traceback.print_exc()
        abort(400)

@PublicAPI.route('/getlocalcert/<remote_id>', methods=['GET'])
def get_local_cert(remote_id):
    print("get_local_cert")
    try:
        assert remote_id == request.view_args['remote_id']
        homevee_server = HomeveeServer(remote_id)
        
        return json.dumps({'local_cert': homevee_server.get_cert()})
    except:
        traceback.print_exc()
        abort(400)

@PublicAPI.route('/getcloudcert/<ip_address>', methods=['GET'])
def get_cloud_cert(ip_address):
    print("get_cloud_cert")
    try:
        assert ip_address == request.view_args['ip_address']
        homevee_cloud = HomeveeCloud(ip_address)

        return json.dumps({'cloud_cert': homevee_cloud.get_cert()})
    except:
        traceback.print_exc()
        abort(400)

@PublicAPI.route('/getusedcloud/<remote_id>', methods=['GET'])
def get_used_cloud(remote_id):
    print("get_used_cloud")
    try:
        assert remote_id == request.view_args['remote_id']
        homevee_server = HomeveeServer(remote_id)

        return json.dumps({'cloud': homevee_server.get_cloud()})
    except:
        traceback.print_exc()
        abort(400)

@PublicAPI.route('/processdata/<remote_id>', methods=['POST'])
def process_data(remote_id):
    print("process_data")
    if Utils.azureCloudNode is None:
        Utils.azureCloudNode = CloudNode.init_cloud_node()

    assert remote_id == request.view_args['remote_id']

    data = request.get_json()

    try:
        return Utils.azureCloudNode.send_to_homevee_hub(remote_id, data)
    except:
        traceback.print_exc()
        abort(400)