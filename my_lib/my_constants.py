# encoding: utf-8
import os
import sys

from configparser import ConfigParser

from my_environment import get_short_hostname, get_hostname_long, get_dc_location, get_environment

__version__ = "01.20201207.01"


Conf = ConfigParser()
ConfFile = "config.conf"

if os.path.exists(ConfFile):
	Conf.read(ConfFile)
else:
	raise TypeError(f"Falha ao ler arquivo de config.conf na raiz do projeto")

SCRIPT_FRIENDLYNAME = Conf.get("APP", "SCRIPT_FRIENDLYNAME")
VERSION_APP = Conf.get("APP", "VERSION_APP")
ROOT_PATH = os.path.abspath(os.getcwd())
MODULE_PATH = Conf.get("PATH", "MODULES_PATH")
LOGGING_DIR = os.path.join(ROOT_PATH, "logs")
LOGGING_NAME_PATH = os.path.join(LOGGING_DIR, SCRIPT_FRIENDLYNAME + ".log")
START_SCRIPT_MESSAGE = " BEGIN ".center(72, "=")
END_SCRIPT_MESSAGE = " END ".center(72, "=")
HOSTNAME = get_short_hostname()
HOSTNAME_LONG = get_hostname_long()
ENVIRONMENT = get_environment(HOSTNAME)
LOCATION = get_dc_location(HOSTNAME)

if __name__ == "__main__":
	print(SCRIPT_FRIENDLYNAME)
	print(VERSION_APP)
	print(MODULE_PATH)