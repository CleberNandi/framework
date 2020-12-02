# encoding: utf-8
import inspect
import smtplib
import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
from email.mime.application import MIMEApplication

from my_constants import HOSTNAME, ENVIRONMENT, LOCATION, SCRIPT_FRIENDLYNAME
from my_message import print_message

__version__ = "01.20201126.01"

def GetSmtpServerAndPortGmail():
    SmtpServer = "smtp.gmail.com"
    SmtpPort = 587
    
    return SmtpServer, SmtpPort

def SendEmailGmail(StrFromAddress, StrSubject, StrMessage, StrPriority, ListToAddress=[], ListAttach=[]):
    Subject = StrSubject
    Message = StrMessage
    Priority = StrPriority
    SmtpServer, SmtpPort = GetSmtpServerAndPortGmail()    
    FromAddress = StrFromAddress
    Password = os.getenv("PasswordGmail")
    ToAddress = ListToAddress
    
    if Priority.upper() == "HIGH":
        Priority = "1"
    elif Priority.upper() == "LOW":
        Priority = "5"
    else:
        Priority = "3" #  NORMAL
    
    Text = MIMEText(Message, "html")
    Header = MIMEMultipart()
    
    # Caso tenha anexos
    if ListAttach:
        for Attach in ListAttach:
            Base = MIMEBase("application", "octet-stream") 
            Base.set_payload(open(Attach, "rb").read())
            encoders.encode_base64(Base)
            AttachFileName = os.path.split(Attach)
            Base.add_header("Content-Disposition", "attachment; filename="+str(AttachFileName[1]))
            Header.attach(Base)
    
    Header.attach(Text)
    Header["Subject"] = Subject
    Header["From"] = FromAddress
    Header["To"] = ",".join(ToAddress)
    Header["Date"] = formatdate(localtime=True)
    Header["X-Priority"] = Priority
    
    try:
        Smtp = smtplib.SMTP(SmtpServer, SmtpPort)
        Smtp.ehlo()
        Smtp.starttls()
        Smtp.ehlo()
        Smtp.login(FromAddress, Password)
        Smtp.sendmail(FromAddress, ToAddress, Header.as_string())
        Smtp.quit()
        print_message("Email enviado com sucesso", "OK")
    except Exception as ErrorEmail:
        print_message(f"Falha ao enviar email. Erro: {ErrorEmail}", "W")
            

def GetSmtpServerAndPort():
    SmtpServer = "smtpdc.dominiosistemas.com.br"
    SmtpPort = 25
    
    if LOCATION == "LCW":
        SmtpServer = "smtpdc.dominiosistemas.com.br"
    elif LOCATION == "SKY":
        SmtpServer = "smtp01.dominioweb.local"
    elif LOCATION == "AZV":
        SmtpPort = 587
        SmtpServer = "172.205.3.181" #  AZV PROD
        
        if ENVIRONMENT == "CI": #  CI
            SmtpServer = "172.200.48.95" #  AZV CI (DW011VW-CI-AZV)
        elif ENVIRONMENT == "DM": #  DEMO
            SmtpServer = "172.200.48.95" #  AZV DEMO
        elif ENVIRONMENT == "QD": #  QED
            SmtpServer = "172.200.179.81" #  AZV QED
    else:
        SmtpServer = "smtpdc.dominiosistemas.com.br"
    
    return SmtpServer, SmtpPort

def SendEmail(StrFromAddress, StrSubject, StrMessage, StrPriority, ListToAddress=[], ListAttach=[]):
    Subject = StrSubject
    Message = StrMessage
    Priority = StrPriority
    SmtpServer, SmtpPort = GetSmtpServerAndPort()    
    FromAddress = StrFromAddress
    ToAddress = ListToAddress
    
    if Priority.upper() == "HIGH":
        Priority = "1"
    elif Priority.upper() == "LOW":
        Priority = "5"
    else:
        Priority = "3" #  NORMAL
    
    Text = MIMEText(Message, "html")
    Header = MIMEMultipart()
    
    # Caso tenha anexos
    if ListAttach:
        for Attach in ListAttach:
            Base = MIMEBase("application", "octet-stream") 
            Base.set_payload(open(Attach, "rb").read())
            encoders.encode_base64(Base)
            AttachFileName = os.path.split(Attach)
            Base.add_header("Content-Disposition", "attachment; filename="+str(AttachFileName[1]))
            Header.attach(Base)
    
    Header.attach(Text)
    Header["Subject"] = Subject
    Header["From"] = FromAddress
    Header["To"] = ",".join(ToAddress)
    Header["Date"] = formatdate(localtime=True)
    Header["X-Priority"] = Priority
    
    try:
        Smtp = smtplib.SMTP(SmtpServer, SmtpPort)
        Smtp.sendmail(FromAddress, ToAddress, Header.as_string())
        Smtp.quit()
        print_message("Email enviado com sucesso", "OK")
    except Exception as ErrorEmail:
        print_message(f"Falha ao enviar email. Erro: {ErrorEmail}", "W")

def SendEmailInfo(StrSubject, StrMessage, StrPriority, ListToAddress=[], ListAttach=[]):
    Subject = HOSTNAME + "::" + SCRIPT_FRIENDLYNAME + "::" + StrSubject
    FromAddress = "ListIncludedClientsWithgroups.Info <listincludedclientswithgroups.info@dominiosistemas.com.br>"
    
    SendEmail(StrFromAddress=FromAddress, 
              StrSubject=Subject, 
              StrMessage=StrMessage, 
              StrPriority=StrPriority, 
              ListToAddress=ListToAddress,
              ListAttach=ListAttach)

def SendEmailWarnig(StrSubject, StrMessage, StrPriority, ListToAddress=[], ListAttach=[]):
    Subject = HOSTNAME + "::" + SCRIPT_FRIENDLYNAME + "::" + StrSubject
    FromAddress = "ListIncludedClientsWithEngine.Warning <listincludedclientswithengine.warning@dominiosistemas.com.br>"
    
    SendEmail(StrFromAddress=FromAddress, 
              StrSubject=Subject, 
              StrMessage=StrMessage, 
              StrPriority=StrPriority, 
              ListToAddress=ListToAddress,
              ListAttach=ListAttach)

def SendEmailError(StrSubject, StrMessage, StrPriority, ListToAddress=[], ListAttach=[]):
    Subject = HOSTNAME + "::" + SCRIPT_FRIENDLYNAME + "::" + StrSubject
    FromAddress = "ListIncludedClientsWithEngine.Error <listincludedclientswithengine.error@dominiosistemas.com.br>"
    
    SendEmail(StrFromAddress=FromAddress, 
              StrSubject=Subject, 
              StrMessage=StrMessage, 
              StrPriority=StrPriority, 
              ListToAddress=ListToAddress,
              ListAttach=ListAttach)
