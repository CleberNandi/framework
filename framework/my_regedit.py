# -*- utf-8 -*-
import os
import winreg

from winreg import ConnectRegistry, OpenKey, EnumKey, EnumValue, QueryValue, OpenKeyEx, SetValueEx
from winreg import KEY_WRITE, KEY_WOW64_32KEY, KEY_WOW64_64KEY, CloseKey

from framework.my_message import print_message

__version__ = "20201202.01"
 
def connect_root_key(root_key: object) -> object:
	connect: object = None
	
	try:
		root_key: object = ConnectRegistry(None, root_key)
		connect = root_key
		print_message(f"root key conectada com sucesso.")
	except WindowsError:
		pass
	except Exception as error_root_key:
		print_message(f"Falha ao tentar conectar em root key. Erro: {error_root_key}", "E")
	
	return connect

def open_key_in_path(connect_root_key: object, 
					 path_key: str) -> object:
	open_key: object = None
	
	try:
		open_key = OpenKey(connect_root_key, path_key)
		print_message(f"Chave {path_key} aberta com sucesso.")
	except WindowsError:
		pass
	except Exception as error_open_key:
		print_message(f"Falha ao tentar abrir chave {path_key}. Erro: {error_open_key}", "E")

	return open_key

def get_key_recursive(connect_root_key: object) -> str:
	index: int = 0

	try:
		while True:
			yield EnumKey(connect_root_key, index)
			index += 1
	except WindowsError:
		pass

def get_register_recursive(connect_root_key: object, 
						   path_key: str) -> str:
	try:
		connect_root_key = OpenKey(connect_root_key, path_key)

		for key_sub in get_key_recursive(connect_root_key):
			key_full = f'{path_key}\\{key_sub}'
			yield key_full
			yield from get_register_recursive(connect_root_key, key_full)
	except WindowsError:
		pass
	except Exception as error_register_recursive:
		print_message(f"Falha ao fazer recursividade do registro {error_register_recursive}", "E")

def get_register_value_recursive(connect_root_key: object, 
								 path_key: str, 
								 search: dict = None) -> dict:
	values: dict = {}
	for key_path in get_register_recursive(connect_root_key, path_key):
		root_key = OpenKey(connect_root_key, key_path)
		if search:
			for search_key in search.items():
				if search_key in key_path.split("\\")[-1]:
					values[key_path] = QueryValue(root_key, None)
	return values

def sub_keys(connect_root_key: object) -> str:
	index: int = 0
 
	while True:
		try:
			subkey = EnumKey(connect_root_key, index)
			yield subkey
			index += 1
		except WindowsError:
			break

def get_values(root_key: object) -> dict:
	key_dict: dict = {}
	index: int = 0
 
	while True:
		try:
			subvalue = EnumValue(root_key, index)
		except WindowsError:
			break
		key_dict[subvalue[0]] = subvalue[1:]
		index += 1
	return key_dict

def search_registry_way(root_key: object, 
						keypath: str, 
						key_path_list: list, 
						search_key: str = None, 
						search_value: str = None) -> list:
	open_key: object = OpenKey(root_key, keypath)
	
	try:
		search_list = list(get_values(open_key).items())
		
		if search_key:
			if search_key in keypath.split("\\")[-1]:
				if search_value:
					try:
						search_list = search_list[0][1][0]
						
						if search_value in search_list.split("\\"):
							key_path_list.append(keypath)
					except IndexError:
						pass
		for subkey in sub_keys(open_key):
			subkeypath = "%s\\%s" % (keypath, subkey)
			search_registry_way(root_key, subkeypath, key_path_list, search_key, search_value)
	except WindowsError:
		pass
	except Exception as error:
		print(f"Falha ao trazer lista. Erro: {error}")
	
	return key_path_list

def set_key_reg(connect_root_key: object, 
			  key_path: str, 
			  key_value_name: str, 
			  key_type: object, 
			  key_value_data: str) -> bool:
	seeArchPath: list = key_path.split("\\") 
	open_key: object = None

	if "Wow6432Node" in seeArchPath:
		flagArchKey = KEY_WOW64_32KEY
	else:
		flagArchKey = KEY_WOW64_64KEY
		
	try:
		open_key = OpenKeyEx(connect_root_key, key_path, access=KEY_WRITE | flagArchKey)
		print_message("Registro localizado com sucesso", "OK")
		try: 
			SetValueEx(open_key, key_value_name, 0, key_type, key_value_data)
			print_message(f"Nome Valor: {key_value_name}")
			print_message(f"Valor: {key_value_data}")
			print_message("Adicionado com sucesso", "OK")
			print_message("-------------------------------------------------------------------------")
		except Exception as err:
			print_message(f"Nome Valor: {key_value_name}")
			print_message(f"Valor: {key_value_data}")
			print_message(f"Erro: {err}")
			print_message("Não foi possível inserir ou alterar valor do registro informado", "W")
			print_message("-------------------------------------------------------------------------")
	except FileNotFoundError:
		print_message("Registro não foi localizado. Tentando criar registro informado", "E")
		try:
			open_key = winreg.CreateKeyEx(connect_root_key, key_path, access=winreg.KEY_WRITE | flagArchKey)
			print_message("Registro criado com sucesso.")
			try: 
				SetValueEx(open_key, key_value_name, 0, key_type, key_value_data)
				print_message(f"Nome Valor: {key_value_name}")
				print_message(f"Valor: {key_value_data}")
				print_message("Adicionado com sucesso", "OK")
				print_message("-------------------------------------------------------------------------")
			except Exception as err:
				print_message(f"Nome Valor: {key_value_name}")
				print_message(f"Valor: {key_value_data}")
				print_message(f"Erro: {err}")
				print_message("Não foi possível inserir ou alterar valor do registro informado", "W")
				print_message("-------------------------------------------------------------------------")
		except Exception as err:	
			print_message("Mensagem: Não foi possível criar registro informado.", "E")
			print_message(f"Erro: {err}.", "E")
			print_message("-------------------------------------------------------------------------")

if __name__ == "__main__":
	print_message("Estou no módulo que trata as chaves do regedit", "OK")