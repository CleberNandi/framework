# encoding: utf-8
from time import strftime

from framework.my_message import print_message

__version__ = "01.20201207.01"

def get_date_time() -> str:
    return strftime("%Y%m%d-%H%M")

if __name__ == "__main__":
	print_message("Estou no módulo que trata as chaves do regedit", "OK")