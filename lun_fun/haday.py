import sys
import random
from datetime import date
from lun_fun import main_commands

def takeaday(this_year=True):
    unit_century = 100*365+25
    offset_this_century = unit_century*20
    offset_start = offset_this_century
    dat = date.fromordinal(random.randint(offset_start-unit_century*2, offset_start+unit_century*2))
    if this_year:
        dat = date(date.today().year, dat.month, dat.day)
    return dat

@main_commands.command()
def haday():
    """是星期几呀？"""
    while True:
        dat = takeaday()
        print(f"What is the weekday of {dat.isoformat()}?")
        while True:
            # 作答
            enput = input("Answer:")
            if enput.lower() in {'q', 'quit', 'exit'}:
                sys.exit()
            try:
                n = int(enput) % 7 or 7
            except ValueError:
                print(f"invalid input '{enput}'")
                continue
            if n == dat.isoweekday():
                print("Right. Next.")
                break
            else:
                print("Wrong. Try again.")