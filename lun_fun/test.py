import sys
import unittest
import click
from . import main_commands
from .misc import load_object

@main_commands.command()
@click.argument('module_name', default="*")
def test(module_name):
    """
    测试指定模块
    """
    mod_path = "lun_fun." + module_name
    if module_name == "*":
        mod_path = "lun_fun"
    unittest.main(module=mod_path, argv=[sys.argv[0], "-v"])
