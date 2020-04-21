import MySQLdb
import configparser
import pathlib
import subprocess
import sys
import os.path
# from . import main_commands

def get_conn():
    config = configparser.ConfigParser()
    config.read(pathlib.Path.home()/'lun-fun.ini', encoding='utf8')
    host = config['journal'].get('host')
    port = config['journal'].getint('port')
    db = config['journal'].get('database')
    user = config['journal'].get('database')
    password = config['journal'].get('password')

    conn = MySQLdb.connect(host=host, port=port, db=db, user=user, passwd=password)
    conn.set_character_set("utf8")
    
    return conn

def run_sql(sql, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params)
    rowcount = cur.rowcount
    conn.commit()
    conn.close()
    return rowcount

def get_editor():
    config = configparser.ConfigParser()
    config.read(pathlib.Path.home()/'lun-fun.ini', encoding='utf8')
    editor = config['journal'].get('editor')
    return editor

# @main_commands.command()
def journal():
    """
    记录日志
    """
    cur = get_cursor()

def read_line(f):
    r = f.readline()
    while r.isspace():
        r = f.readline()
    return r

def write():
    with (pathlib.Path.home()/'journal.lixunote').open(encoding='utf8', mode='r') as f:
        pass
    subprocess.run([get_editor(), str(pathlib.Path.home()/'journal.lixunote')])

def save():
    ok = False
    with (pathlib.Path.home()/'journal.lixunote').open(encoding='utf8', mode='r') as f:
        category = read_line(f).strip()
        content = f.read().strip()
        rowcount =  run_sql("insert into journal(`date`, category, content) values(current_date(), %s, %s)", (category, content))
        if rowcount:
            ok = True
    if ok:
        print("Ok.")
        os.remove(str(pathlib.Path.home()/'journal.lixunote'))

if __name__ == '__main__':
    if sys.argv[1] == 'write':
        write()
    elif sys.argv[1] == 'save':
        save()