import MySQLdb
import pathlib
from lun_fun.config import config
from sshtunnel import SSHTunnelForwarder

def make_mysql_connection(config):
    host = config.get('host')
    port = int(config.get('port'))
    db = config.get('database')
    user = config.get('user')
    password = config.get('password')
    conn = MySQLdb.connect(host=host, port=port, db=db, user=user, passwd=password, autocommit=True)
    conn.set_character_set("utf8")
    return conn

class Connection():

    def __init__(self, ssh_username, ssh_private_key_password, database, username, password):
    	"""
    	SSH隧道相当于VPN
    	"""
        self.server = SSHTunnelForwarder(
            'lixulun.top',
            ssh_username=ssh_username,
            ssh_pkey=str(pathlib.Path.home()/'.ssh'/'id_rsa'),
            ssh_private_key_password=ssh_private_key_password,
            remote_bind_address=('localhost', 3306),
        )
        self.database = database
        self.username = username
        self.password = password
        

    def __enter__(self):
        self.server.start()
        self.connection = MySQLdb.connect(host="localhost", port=self.server.local_bind_port, db=self.database, user=self.username, passwd=self.password, autocommit=True)
        self.connection.set_character_set('utf8')
        return self.connection

    def __exit__(self, *args):
        """
        使用ContextManager解决了主线程异常时，SSHTunnelForwarder无法正常退出的问题
        """
        self.connection.close()
        self.server.close()

def get_connection(module):
    conn = Connection(
        ssh_username=config['global']['ssh_username'],
        ssh_private_key_password=config['global']['ssh_private_key_password'],
        database=config[module]['database'],
        username=config[module]['username'],
        password=config[module]['password'],
    )
    return conn