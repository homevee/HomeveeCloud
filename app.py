#!flask/bin/python
import argparse
from _thread import start_new_thread

from flask import Flask
from passlib.handlers.pbkdf2 import pbkdf2_sha512

from cloud import HomeveeCloudNode
from cloud.Database import Database
from cloud.blueprints.AlexaAPI import AlexaAPI
from cloud.blueprints.CloudAPI import CloudAPI
from cloud.blueprints.GoogleHomeAPI import GoogleHomeAPI
from cloud.blueprints.OAuthAPI import OAuthAPI
from cloud.blueprints.PublicAPI import PublicAPI
from cloud.blueprints.rest_api.RestAPI import RestAPI
from cloud.blueprints.ShopAPI import ShopAPI
from cloud.blueprints.ServerAPI import ServerAPI

app = Flask(__name__)

DEV_ENV = True

def update_cert(file):
    cert_data = open(file).read()
    #cert_data = cert_data.replace("\n", "")
    #cert_data = cert_data.replace("-----BEGIN CERTIFICATE-----", "")
    #cert_data = cert_data.replace("-----END CERTIFICATE-----", "")

    Database().do_query("REPLACE INTO CLOUD_CERTS (IP, CERTIFICATE) VALUES (%s, %s)",
                        (args.ip, cert_data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Homevee-Cloud for Servers')
    #parser.add_argument('--ip', required=True, type=str, help='The IP of the Server')
    #parser.add_argument('--max_clients', default=50, type=int, help='Number of clients simultaneously')
    #parser.add_argument('--buffer_size', default=64, type=int, help='Buffer size for client communication')
    #parser.add_argument('--debug', default=False, type=bool, help='Is the server in debug mode?')
    parser.add_argument('--dev', default=False, type=bool, help='Is the server in dev mode?')
    parser.add_argument('--domain', required=False, default="cloud.homevee.de", type=str, help='The domain to run the cloud node on')
    args = parser.parse_args()

    #hashed_access_token = pbkdf2_sha512.encrypt("+4mT6OzDRMQgZY4VX+cQGxnuSzFF4SjNFM+p/L90LdirFP6X0lIPfU8fCtfgUdoA3N+lpepN82UOgvZ/7lwV6BNYdYvNyD9duCFbNtwMpr+x+4WD5Ze0udQGvviN4W5FN4SFZ2eFh9fa2+DQdc1BBRXJKDwDpNPFPpJ1rmKsw1Y=" +
    # "16263821935c66e615a137f9.97473803", rounds=200000)
    #print(hashed_access_token)

    HOST = args.domain

    CERT_FILE = "/etc/letsencrypt/live/" + HOST + "/cert.pem"
    CHAIN_FILE = "/etc/letsencrypt/live/" + HOST + "/chain.pem"
    FULLCHAIN_FILE = "/etc/letsencrypt/live/" + HOST + "/fullchain.pem"
    KEY_FILE = "/etc/letsencrypt/live/" + HOST + "/privkey.pem"

    DEV_ENV = args.dev

    blueprints = [ServerAPI, ShopAPI, RestAPI, PublicAPI, CloudAPI, OAuthAPI, AlexaAPI, GoogleHomeAPI]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    #app.run(debug=True)


    if DEV_ENV:
        app.run(host='0.0.0.0', debug=True)
    else:
        #update_cert(CERT_FILE)

        #HomeveeCloudNode.DOMAIN = HOST
        #HomeveeCloudNode.CLIENT_NUM = args.max_clients
        #HomeveeCloudNode.IS_DEBUG = args.debug
        #HomeveeCloudNode.IP = args.ip
        #HomeveeCloudNode.BUFFER_SIZE = args.buffer_size
        #HomeveeCloudNode.SERVER_SECRET = args.server_secret

        #start_new_thread(HomeveeCloudNode.start, ())

        app.run(host=HOST, port=443, ssl_context=(FULLCHAIN_FILE, KEY_FILE))
