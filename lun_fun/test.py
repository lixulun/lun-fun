import sys
import unittest
import click
from .misc import load_object

@click.command()
@click.argument('module_name')
def test(module_name):
    """
    测试指定模块
    """
    unittest.main(module="lun_fun." + module_name, argv=[sys.argv[0]])
