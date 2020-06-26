import click
from datetime import date as Date
from lun_fun import main_commands

@main_commands.command()
@click.argument('query', default=Date.today().isoformat())
def iwencai(query):
    date = Date.fromisoformat(query)
    print(exp_by_date(date))

def exp_by_date(date):
    last_year_is_full = date.month > 4
    last_year = date.year - 1
    if not last_year_is_full:
        last_year -= 1
    unit_ROE = 3.75
    exps = []
    exps.append(f"{last_year-6}年到{last_year}年ROE>=15%")
    if date.month <= 4 and date.day <= 30:
        ses = 3
        near_date = Date(date.year-1, 9, 30)
    elif date.month <= 8 and date.day <= 31:
        ses = 1
        near_date = Date(date.year, 3, 31)
    elif date.month <= 10 and date.day <= 31:
        ses = 2
        near_date = Date(date.year, 6, 30)
    else:
        ses = 3
        near_date = Date(date.year, 9, 30)
    s_date = get_cn_date(near_date)
    exps.append(f"{s_date}ROE>={unit_ROE * ses}%")
    exps.append(f"上市时间早于{date.year-5}年{date.month}月")
    exps.append("行业")
    exps.append(f"{s_date}营收增长率")
    exps.append(f"{s_date}净利润增长率")
    exps.append(f"{last_year}营收增长率")
    exps.append(f"{last_year}净利润增长率")
    return "，".join(exps)

def get_cn_date(date):
    return f"{date.year}年{date.month}月{date.day}日"