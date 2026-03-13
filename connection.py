import os
import oracledb

def get_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    return oracledb.connect(user=user, password=password, dsn=dsn)