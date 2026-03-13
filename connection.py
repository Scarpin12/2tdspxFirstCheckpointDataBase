import os
import oracledb

def get_connection():
    user = "seu_usuario_aqui"
    password = "sua_senha_aqui"  
    dsn = "oracle.fiap.com.br:1521/orcl"

    return oracledb.connect(user=user, password=password, dsn=dsn)