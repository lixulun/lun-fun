import MySQLdb
import configparser
import pathlib
import subprocess
import sys
import os.path
from .. import main_commands
from ..config import config
from ..connection import make_mysql_connection

path_journal = config['journal'].get('journal-path', pathlib.Path.home()/'journal.lixunote')

def get_editor():
    editor = config['journal'].get('editor')
    return editor

@main_commands.group()
def journal():
    """
    记录日志
    """
    pass

def read_line(f):
    r = f.readline()
    while r.isspace():
        r = f.readline()
    return r

@journal.command()
def write():
    """
    书写/修改未提交的日志
    """
    with path_journal.open(encoding='utf8', mode='a') as f:
        pass
    subprocess.run([get_editor(), str(path_journal)])

def _save(conn):
    sql = """
    INSERT INTO journal(`date`, category, content)
    VALUES(current_date(), %s, %s)
    """
    ok = False
    with path_journal.open(encoding='utf8', mode='r') as f:
        category = read_line(f).strip()
        content = f.read().strip()
        if not category or not content:
            raise ValueError("Empty text is unacceptable.")
        with conn.cursor() as cur:
            cur.execute(sql, (category, content))
            if cur.rowcount:
                ok = True
    if ok:
        print("Ok.")
        os.remove(str(path_journal))

@journal.command()
def save():
    """
    保存至数据库
    """
    conn = make_mysql_connection(config['journal'])
    _save(conn)
    conn.close()

if __name__ == '__main__':
    if sys.argv[1] == 'write':
        write()
    elif sys.argv[1] == 'save':
        conn = make_mysql_connection(config['journal'])
        _save(conn)
        conn.close()