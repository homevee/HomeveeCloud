import mysql.connector

from HomeveeCloud.cloud.Helper import Logger
from HomeveeCloud.cloud.Helper.Utils import Utils

class Database():
    def __init__(self, db=None):
        if db is None:
            db = self.get_database_con()
        self.db = db

    def do_query(self, sql: str, params: dict):
        """
        Executes the given sql-statement and returns a pointer to the resulting cursor
        :param sql: the sql-statement as a string
        :param params: the parameters-dict
        :return: the cursor after executing the query
        """
        mycursor = self.db.cursor()

        Logger.log((sql, params))

        mycursor.execute(sql, params)

        return mycursor

    def get_database_con(self):
        """
        Returns a connection to the database
        :return: the database connection
        """

        data = Utils.get_config_data()

        host = data['db_host']
        user = data['db_user']
        passwd = data['db_password']
        database = data['db_name']

        db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        return db