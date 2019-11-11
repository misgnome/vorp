from .const import *
import psycopg2


class Authorizer:
    def __init__(self):

        self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT)


    def close(self):
        self.conn.close()

