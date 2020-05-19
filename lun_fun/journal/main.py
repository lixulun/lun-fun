import pathlib
import subprocess
import os
import click
from .. import main_commands
from ..config import config
from ..connection import make_mysql_connection

path_journal = config['journal'].get('journal-path', pathlib.Path.home()/'journal.lixunote')

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
    subprocess.run([config['journal'].get('editor', 'notepad'), str(path_journal)])

def _save(conn):
    sql = """
    INSERT INTO journal(`date`, category, title, content)
    VALUES(current_date(), %s, %s, %s)
    """
    ok = False
    with path_journal.open(encoding='utf8', mode='r') as f:
        category = read_line(f).strip()
        title = read_line(f).strip()
        content = f.read().strip()
        if not category or not content:
            raise ValueError("Empty text is unacceptable.")
        with conn.cursor() as cur:
            cur.execute(sql, (category, title, content))
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

def _list(conn):
    sql = """
    SELECT rowid, category, title, `date` 
    FROM journal
    """
    from tabulate import tabulate
    with conn.cursor() as cur:
        cur.execute(sql)
        res = []
        cols = list(map(lambda x: x[0], cur.description))
        for one in cur.fetchall():
            res.append(dict(zip(cols, one)))
        print(tabulate(res, headers='keys'))

@journal.command(name='list')
def j_list():
    """
    列出所有日志信息
    """
    conn = make_mysql_connection(config['journal'])
    _list(conn)
    conn.close()

@journal.command()
@click.argument('_id')
def read(_id):
    """
    阅读指定journal
    """
    sql = """
    SELECT title, content, `date`
    FROM journal
    WHERE rowid=%s
    """
    conn = make_mysql_connection(config['journal'])
    with conn.cursor() as cur:
        cur.execute(sql, (_id,))
        r = cur.fetchone()
        print(f"《{r[0]}》", r[2], "\n")
        print(r[1])
    conn.close()