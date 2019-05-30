from passlib.handlers.pbkdf2 import pbkdf2_sha512

from cloud.Helper.Database import Database


class HomeveeServer():
    def __init__(self, remote_id):
        self.database = Database()
        result = self.database.do_query("SELECT * FROM SERVER_DATA WHERE REMOTE_ID = %s;",
                                   (remote_id,))
        remote_id, hashed_access_token, salt, is_premium, premium_until = result.fetchone()

        self.remote_id = remote_id
        self.hashed_access_token = hashed_access_token
        self.salt = salt
        self.is_premium = (is_premium == 1)
        self.premium_until = premium_until

    def verify_server(self, access_token):
        #print("access_token: "+access_token)
        #print("salt: "+str(self.salt))
        #print("saved hash: "+self.hashed_access_token)
        #print("hashed_access_token: "+pbkdf2_sha512.encrypt(access_token + self.salt, rounds=200000))

        try:
            return pbkdf2_sha512.verify(access_token + self.salt, self.hashed_access_token)
        except:
            return False

    def get_cloud(self):
        result = self.database.do_query("SELECT CLOUD FROM CLOUD_DATA WHERE REMOTE_ID = %s;",
                               (self.remote_id, ))
        cloud, =  result.fetchone()
        return cloud

    def update_cloud(self, cloud):
        self.database.do_query("REPLACE INTO CLOUD_DATA (REMOTE_ID, CLOUD) VALUES (%s,%s);",
                               (self.remote_id, cloud,))

    def set_premium(self, is_premium):
        self.database.do_query("UPDATE SERVER_DATA SET IS_PREMIUM = %s;", (is_premium,))

    def update_ip(self, ip):
        self.database.do_query("REPLACE INTO LOCAL_IPS (REMOTE_ID, IP_ADDRESS) VALUES (%s,%s);",
                               (self.remote_id, ip,))

    def get_ip(self):
        result = self.database.do_query("SELECT IP_ADDRESS FROM LOCAL_IPS WHERE REMOTE_ID = %s;",
                               (self.remote_id, ))
        ip, =  result.fetchone()
        return ip

    def update_cert(self, cert):
        self.database.do_query("REPLACE INTO CERTIFICATES (REMOTE_ID, CERT) VALUES (%s,%s);",
                               (self.remote_id, cert,))

    def get_cert(self):
        result = self.database.do_query("SELECT CERT FROM CERTIFICATES WHERE REMOTE_ID = %s;",
                               (self.remote_id, ))
        cert, =  result.fetchone()
        return cert