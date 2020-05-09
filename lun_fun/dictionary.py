import click
import pprint
from . import main_commands
from .config import config
from .connection import make_mysql_connection

def get(conn, key):
    sql = """
    SELECT `key`, `value`
    FROM dictionary
    WHERE `key` LIKE %s
    """
    result = []
    with conn.cursor() as cur:
        cur.execute(sql, (key,))
        for item in cur.fetchall():
            result.append({
                'key': item[0],
                'value': item[1],
            })
    return result


def _set(conn, key, value):
    sql = """
    INSERT INTO dictionary(`key`, `value`)
    VALUES(%s, %s)
    """
    with conn.cursor() as cur:
        cur.execute(sql, (key, value))

@main_commands.command()
@click.argument('key')
@click.argument('value', default=None, required=False)
def dictionary(key, value):
    """
    存储/检索
    """
    conn = make_mysql_connection(config['dictionary'])
    if value:
        _set(conn, key, value)
    else:
        for item in get(conn, key):
            pprint.pprint(item)
    conn.close()