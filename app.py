#!flask/bin/python
import argparse
from flask import Flask
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Homevee-Cloud for Servers')
    parser.add_argument('--dev', default=False, type=bool, help='Is the server in dev mode?')
    parser.add_argument('--test', default=False, type=bool, help='Is the server in test mode?')
    parser.add_argument('--domain', required=False, default="cloud.homevee.de", type=str, help='The domain to run the cloud node on')
    args = parser.parse_args()

    HOST = args.domain

    CERT_FILE = "/etc/letsencrypt/live/" + HOST + "/cert.pem"
    CHAIN_FILE = "/etc/letsencrypt/live/" + HOST + "/chain.pem"
    FULLCHAIN_FILE = "/etc/letsencrypt/live/" + HOST + "/fullchain.pem"
    KEY_FILE = "/etc/letsencrypt/live/" + HOST + "/privkey.pem"

    DEV_ENV = args.dev
    TEST_ENV = args.test

    blueprints = [ServerAPI, ShopAPI, RestAPI, PublicAPI, CloudAPI, OAuthAPI, AlexaAPI, GoogleHomeAPI]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    if DEV_ENV:
        app.run(debug=True)
    elif TEST_ENV:
        HOST = "dev-test.homevee.de"

        CERT_FILE = "/etc/letsencrypt/live/" + HOST + "/cert.pem"
        CHAIN_FILE = "/etc/letsencrypt/live/" + HOST + "/chain.pem"
        FULLCHAIN_FILE = "/etc/letsencrypt/live/" + HOST + "/fullchain.pem"
        KEY_FILE = "/etc/letsencrypt/live/" + HOST + "/privkey.pem"

        app.run(host=HOST, port=7777, ssl_context=(FULLCHAIN_FILE, KEY_FILE))
    else:
        app.run(host=HOST, port=443, ssl_context=(FULLCHAIN_FILE, KEY_FILE))
