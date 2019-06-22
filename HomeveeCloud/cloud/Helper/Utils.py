import base64
import json
import os

from passlib.handlers.pbkdf2 import pbkdf2_sha512


class Utils():

    azureCloudNode = None

    def __init__(self):
        return

    @staticmethod
    def is_cloud_verified(cloud, access_token):
        return False

    @staticmethod
    def generate_access_token():
        # generate access_token
        random_bytes = os.urandom(128)
        access_token = base64.b64encode(random_bytes).decode('utf-8')

        salt = os.urandom(12).hex()

        hashed_access_token = pbkdf2_sha512.encrypt(access_token + salt, rounds=200000)

        return(access_token, hashed_access_token, salt)

    @staticmethod
    def get_config_data():
        with open('/homevee_cloud_data/config.json') as json_file:
            data = json.load(json_file)
            print(data)
            return data