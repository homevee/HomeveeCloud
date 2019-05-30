#!flask/bin/python
import traceback

from flask import Blueprint, abort, request

from cloud.HomeveeServer import HomeveeServer
from cloud.Helper.ServerData import ServerData

ShopAPI = Blueprint('ShopAPI', __name__, template_folder='templates')

HOMEVEE_SHOP_TOKEN = ServerData.get("HOMEVEE_SHOP_TOKEN")

@ShopAPI.route('/setpremium/<remote_id>', methods=['PUT'])
def set_premium(remote_id):
    print("ispremium")
    try:
        assert remote_id == request.view_args['remote_id']
        homevee_server = HomeveeServer(remote_id)
        shop_secret = request.headers['Shop-Secret']
        if shop_secret == ServerData.get("HOMEVEE_SHOP_TOKEN"):
            data = request.get_json()
            is_premium = data['is_premium']
            homevee_server.set_premium(is_premium)
        else:
            abort(401)
    except:
        traceback.print_exc()
        abort(500)