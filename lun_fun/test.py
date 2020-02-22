import sys
import unittest
import click
from . import main_commands
from .misc import load_object

@main_commands.command()
@click.argument('module_name')
def test(module_name):
    """
    测试指定模块
    """
    unittest.main(module="lun_fun." + module_name, argv=[sys.argv[0]])
