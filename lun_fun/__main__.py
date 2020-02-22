import sys
import click
from .misc import load_object, walk_modules

@click.group()
def cli():
    pass

def execute():
    mods = walk_modules("lun_fun")
    print(mods)
    for mod in mods:
        for attr in mod.__dict__:
            attr = getattr(mod, attr)
            if isinstance(attr, click.Command):
                cli.add_command(attr)
    cli()

if __name__ == "__main__":
    execute()