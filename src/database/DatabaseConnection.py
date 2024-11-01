import mysql.connector
from mysql.connector import Error
from threading import local
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseConnection:
    _local = local()

    @classmethod
    def get_connection(cls):
        if not hasattr(cls._local, 'connection'):
            cls._local.connection = cls._create_connection()
        return cls._local.connection
    
    @classmethod
    def _create_connection(cls):
        try:
            connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            return connection
        except Error as e:
            print("Error while connecting to MySQL", e)
            return None