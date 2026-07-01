import pymysql

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        port=3307,
        database="fastapi_db",
        cursorclass=pymysql.cursors.DictCursor
    )