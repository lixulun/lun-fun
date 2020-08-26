import pathlib
import subprocess
import os
import click
import tkinter as tk
from .. import main_commands
from ..config import config
from ..connection import get_connection

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
    with get_connection('journal') as conn:
        _save(conn)

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
    with get_connection('journal') as conn:
        _list(conn)

@journal.command()
@click.option('--window/--text', default=True, help="显示模式")
@click.argument('_id')
def read(_id, window):
    """
    阅读指定journal
    """
    sql = """
    SELECT title, content, `date`
    FROM journal
    WHERE rowid=%s
    """
    with get_connection('journal') as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (_id,))
            r = cur.fetchone()
            title = r[0]
            date = r[2]
            text = r[1]
            if window:
                root = tk.Tk()
                root.title(title + " - " + str(date))
                root.geometry('500x600')
                app = Reader(root, text)
                app.mainloop()
            else:
                print(f"《{r[0]}》", r[2], "\n")
                print(r[1])

class Reader(tk.Text):
    def __init__(self, master=None, text=''):
        super().__init__(master)
        self.master = master
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.insert("1.0", text)
        self.grid(column=0, row=0, sticky=(tk.W, tk.S, tk.N, tk.E))