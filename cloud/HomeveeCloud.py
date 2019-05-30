from passlib.handlers.pbkdf2 import pbkdf2_sha512

from cloud.Database import Database


class HomeveeCloud():
    def __init__(self, ip_address):
        self.database = Database()
        result = self.database.do_query("SELECT * FROM CLOUDS WHERE CLOUD_IP = %s;",
                                   (ip_address,))
        ip_address, is_premium, max_users, is_active = result.fetchone()

        self.ip_address = ip_address
        self.is_premium = (is_premium == 1)
        self.max_users = max_users
        self.is_active = is_active

    def get_cert(self):
        result = self.database.do_query("SELECT CERTIFICATE FROM CLOUD_CERTS WHERE IP = %s;",
                                        (self.ip_address,))
        cert, = result.fetchone()
        return cert

    def get_assigned_client_num(self):
        result = self.database.do_query("SELECT COUNT(*) FROM CLOUD_DATA WHERE CLOUD_IP = %s;",
                               (self.ip_address, ))
        cloud, =  result.fetchone()
        return cloud