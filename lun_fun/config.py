import configparser
import pathlib

path_ini = pathlib.Path.home()/'lun-fun.ini'

config = configparser.ConfigParser()
# 使用List参数是常规用法，单文件名不能兼容以前版本的configparser
config.read([path_ini], encoding='utf8')