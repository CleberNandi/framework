# encoding: utf-8
import inspect
import os
import sys

from framework.my_message import print_message

__version__ = "01.20201207.01"

def is_str_no_blank(text: str) -> bool:
    text_blank = False
    text = text
    
    if text and text.strip():
        text_blank = True
    
    return text_blank

def non_blank_lines(file: str) -> list:
    for line_in in file:
        line = line_in.rstrip()
        if line:
            yield line

def list_files_on_dir(directory: str) -> list:
    files: list = []
    
    try:
        for file in os.listdir(directory):
            filename_full = os.path.join(directory, file)
            
            if os.path.isfile(filename_full):
                files.append(filename_full)
    except Exception as error_files:
        print_message(f"Falha ao listar arquivos. Erro: {error_files}")
    
    return files

def load_list_from_file(file_path: str) -> tuple:
    files: list = []
    num_return: int = 0
    
    try:
        with open(file_path, "r") as file:
            for line in non_blank_lines(file):
                files.append(line)
    except Exception as error_load_list:
        print_message(f"Erro ao carregar arquivo {file_path}. Erro: {error_load_list}", "E")
        num_return = 1
    
    return num_return, files

def save_list_to_file(files: list,
                      filename: str,
                      truncate: bool = False):
    save_file: bool = True
    open_mode = "a"
    
    if truncate:
        open_mode = "w"
    
    try:
        with open(filename, open_mode)as file:
            for line in files:
                file.write(line + "\n")
    except Exception as error_save_list:
        print_message(f"Falha ao salvar lista em arquivo: {filename}. Erro: {error_save_list}")
        save_file = 1
    
    return save_file
            
if __name__ == "__main__":
	print_message("Estou no módulo que trata os textos", "OK")