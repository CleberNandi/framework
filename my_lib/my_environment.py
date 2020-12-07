# encoding: utf-8
import inspect
import os
import socket
import sys

__version__ = "01.20201125.01"

def get_hostname_long():
    return socket.getfqdn()

def get_short_hostname():
    Result = ""
    Hostname = socket.gethostname().upper()
    
    if Hostname.split("."):
        Result = Hostname.split(".")[0]
    
    return Result

def get_environment(StrHostname):
    Result = "PD"
    ListTemp = StrHostname.split("-")
    
    if len(ListTemp) > 2:
        Result = ListTemp[1].upper()    
    elif StrHostname[:11] == "DOMINIO-APP" or StrHostname == "SRV-AD-A" or StrHostname == "SRV-AD-B":
        Result = "PD"
    
    return Result

def get_dc_location(StrHostname):
    Result = "LCW"
    ListHostname = StrHostname.split("-")
    
    if StrHostname[:11] == 'DOMINIO-APP' or StrHostname == 'SRV-AD-A' or StrHostname == 'SRV-AD-B':
        Result = "SKY"
    elif len(ListHostname) > 2:
        Result = ListHostname[2].upper()
    else:
        Result = "LCW"
    
    return Result
    

def main():
    ...

if __name__ == "__main__":
    main()