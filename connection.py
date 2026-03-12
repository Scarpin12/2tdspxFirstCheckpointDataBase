import oracledb

def get_connection():
    user = "seu usuario_do_banco"
    password = "sua_senha_do_banco" 
    dsn = "oracle.fiap.com.br:1521/orcl"

    return oracledb.connect(user=user, password=password, dsn=dsn)