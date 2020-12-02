#-*- utf-8 -*-
import datetime
import inspect
import logging
import os
import sys

from configparser import ConfigParser
from time import strftime

from my_constants import LOGGING_DIR, LOGGING_NAME_PATH

__version__ = "01.20201125.01"

TermColor = {
	'HEADER': '\033[95m',
	'OKBLUE': '\033[94m',
	'OKGREEN': '\033[92m',
	'WARNING': '\033[1;33m',
	'FAIL': '\033[1;31m',
	'ENDC': '\033[0;0m',
	'BOLD': '\033[1m',
	'UNDERLINE': '\033[4m'
}


def print_message(StrMessage: str, StrMessageType: str="I", LogOnly: bool=False):
	str_date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	MessageType = StrMessageType.upper()
	Message = str(StrMessage)

	try:
		MessageInfo = Message + TermColor["ENDC"]
		MessageError = TermColor["FAIL"] + Message + TermColor["ENDC"]
		MessageWarnig = TermColor["WARNING"] + Message + TermColor["ENDC"]
		MessageOk = TermColor["OKGREEN"] + Message + TermColor["ENDC"]

		LoggingMessage = {
			"I": [logging.info, MessageInfo],
			"OK": [logging.info, MessageOk],
			"W": [logging.warning, MessageWarnig],
			"E": [logging.error, MessageError],
		}

		# LoggingMessage[MessageType][0](str(Message, encoding="1252"))
		LoggingMessage[MessageType][0](Message
                                 		.encode(encoding='utf-8', errors='strict')
										.decode(encoding="1252", errors="strict")
                                    )
		if not LogOnly:
			print(f"{str_date_now} #{MessageType}# {LoggingMessage.get(MessageType)[1]}")
	except Exception as Error_print:
		print(f"Erro em PrintMessage. Erro: {Error_print}")

try:
    os.mkdir(LOGGING_DIR)
except FileExistsError:
    pass

logging.basicConfig(
	filename=LOGGING_NAME_PATH, filemode="a", 
	level=logging.INFO, 
	format="%(asctime)s - %(levelname)s - %(message)s", 
	datefmt="%Y-%m-%d %H:%M:%S"
)
   
if __name__ == "__main__":
	print_message("Estou no módulo que trata mensagens.", "OK")