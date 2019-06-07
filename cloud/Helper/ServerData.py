from cloud.Helper.Database import Database

class ServerData():
    def __init__(self):
        return

    @staticmethod
    def get(key):
        database = Database()

        result = database.do_query("SELECT DATA_VALUE, DATA_VALUE FROM KEY_VALUE WHERE DATA_KEY = %s", (key,))

        key, value = result.fetchone()

        return value

    @staticmethod
    def set(key, value):
        database = Database()

        result = database.do_query("REPLACE INTO KEY_VALUE (DATA_KEY, DATA_VALUE) VALUES (%s, %s)", (key,value))