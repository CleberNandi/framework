# encoding: utf-8
from configparser import ConfigParser
from time import strftime

from my_message import print_message

__version__ = "01.20201126.01"

def GetDateTime():
    return strftime("%Y%m%d-%H%M")

if __name__ == "__main__":
	print_message("Estou no módulo que trata as chaves do regedit", "OK")