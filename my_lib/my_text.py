# encoding: utf-8
import inspect
import os
import sys

from configparser import ConfigParser

from my_message import print_message

__version__ = "01.20201126.01"

def IsStrNoBlank(StrText):
    Result = False
    Text = StrText
    
    if Text and Text.strip():
        Result = True
    
    return Result

def NonBlankLines(StrFile):
    File = StrFile
    for LineIn in File:
        Line = LineIn.rstrip()
        if Line:
            yield Line

def ListFilesOnDir(StrDir):
    Dir = StrDir
    Files = []
    
    try:
        for file in os.listdir(Dir):
            FilenameFull = os.path.join(Dir, file)
            
            if os.path.isfile(FilenameFull):
                Files.append(FilenameFull)
    except Exception as ErrorFiles:
        print_message(f"Falha ao listar arquivos. Erro: {ErrorFiles}")
    
    return Files

def LoadListFromFile(StrFilePath):
    FilePath = StrFilePath
    Result = []
    NumReturn = 0
    
    try:
        with open(FilePath, "r") as File:
            for line in NonBlankLines(File):
                Result.append(line)
    except Exception as ErrorLoadList:
        print_message(f"Erro ao carregar arquivo {FilePath}. Erro: {ErrorLoadList}", "E")
        NumReturn = 1
    
    return NumReturn, Result

def SaveListToFile(ListIn, StrFilename, BoolTruncate=False):
    ListIn = ListIn
    Filename = StrFilename
    Result = 0
    OpenMode = "a"
    
    if BoolTruncate:
        OpenMode = "w"
    
    try:
        with open(Filename, OpenMode)as File:
            for Line in ListIn:
                File.write(Line + "\n")
    except Exception as ErrorSaveList:
        print_message(f"Falha ao salvar lista em arquivo: {Filename}. Erro: {ErrorSaveList}")
        Result = 1
    
    return Result
            
if __name__ == "__main__":
	print_message("Estou no módulo que trata os textos", "OK")