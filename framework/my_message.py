#-*- utf-8 -*-
import datetime
import inspect
import logging
import os
import sys

from time import strftime

from framework.my_constants import LOGGING_DIR, LOGGING_NAME_PATH

__version__ = "01.20201125.01"

term_color = {
	'HEADER': '\033[95m',
	'OKBLUE': '\033[94m',
	'OKGREEN': '\033[92m',
	'WARNING': '\033[1;33m',
	'FAIL': '\033[1;31m',
	'ENDC': '\033[0;0m',
	'BOLD': '\033[1m',
	'UNDERLINE': '\033[4m'
}


def print_message(message: str,
                  message_type: str="I",
                  log_only: bool=False):
	str_date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	message_type = message_type.upper()

	try:
		message_info = message + term_color["ENDC"]
		message_error = term_color["FAIL"] + message + term_color["ENDC"]
		message_warnig = term_color["WARNING"] + message + term_color["ENDC"]
		message_ok = term_color["OKGREEN"] + message + term_color["ENDC"]

		LoggingMessage = {
			"I": [logging.info, message_info],
			"OK": [logging.info, message_ok],
			"W": [logging.warning, message_warnig],
			"E": [logging.error, message_error],
		}

		# LoggingMessage[message_type][0](str(message, encoding="1252"))
		LoggingMessage[message_type][0](message
                                 		.encode(encoding='utf-8', errors='strict')
										.decode(encoding="1252", errors="strict")
                                    )
		if not log_only:
			print(f"{str_date_now} #{message_type}# {LoggingMessage.get(message_type)[1]}")
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