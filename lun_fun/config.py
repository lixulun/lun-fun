import configparser
import pathlib

path_ini = pathlib.Path.home()/'lun-fun.ini'

config = configparser.ConfigParser()
config.read(path_ini, encoding='utf8')