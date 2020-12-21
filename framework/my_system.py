# encoding: utf-8
from subprocess import Popen, PIPE
from time import strftime
from typing import Any

from framework.my_message import print_message

__version__ = "01.20201221.01"

class Cmd:
    def __init__(self, cmd:str) -> None:
        self.cmd = cmd
    
    def __call__(self, *args:Any) -> Any:
        command = f"{self.cmd} {' '.join(args)}"
        output = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        return output.communicate()

class Command:
    def __getattr(self, attribute=str) -> tuple:
        return Cmd(attribute)

def get_date_time() -> str:
    return strftime("%Y%m%d-%H%M")

if __name__ == "__main__":
	print_message("Estou no módulo que trata as chaves do regedit", "OK")