import sys
import click
from .misc import load_object, walk_modules

@click.group()
def cli():
    pass

def execute():
    mods = walk_modules("lun_fun")
    for mod in mods:
        if 'exports' in mod.__dict__:
            for com in mod.exports:
                cli.add_command(com)
    cli()

if __name__ == "__main__":
    execute()