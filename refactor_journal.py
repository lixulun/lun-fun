from lun_fun.connection import make_mysql_connection
from lun_fun.config import config

"""
如果title为空，提取content的第一行数据作为title
"""

conn = make_mysql_connection(config['journal'])
res = []
with conn.cursor() as cur:
    cur.execute("select rowid, content from journal where isnull(title)")
    res = cur.fetchall()
    
for t in res:
    rid = t[0]
    title = t[1].splitlines()[0].strip()
    content = '\n'.join(t[1].splitlines()[1:]).strip()
    with conn.cursor() as cur:
        cur.execute("update journal set title=%s, content=%s where rowid=%s", (title, content, rid))
        if cur.rowcount:
            print(f"{rid} changed")
conn.close()