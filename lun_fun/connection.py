import MySQLdb
import configparser

def make_mysql_connection(config):
    host = config.get('host')
    port = int(config.get('port'))
    db = config.get('database')
    user = config.get('user')
    password = config.get('password')
    conn = MySQLdb.connect(host=host, port=port, db=db, user=user, passwd=password, autocommit=True)
    conn.set_character_set("utf8")
    return conn