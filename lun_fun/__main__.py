import sys
from . import main_commands
from .misc import load_object, walk_modules

def execute():
    mods = walk_modules("lun_fun")
    main_commands()

if __name__ == "__main__":
    execute()