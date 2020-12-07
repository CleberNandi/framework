# encoding: utf-8
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

__version__ = "01.20201207.01"

def get_smtp_server_and_port_gmail() -> tuple(str, str):
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    
    return smtp_server, smtp_port

def get_priority_email(priority: str) -> str:
    if priority.upper() == "HIGH":
        priority = "1"
    elif priority.upper() == "LOW":
        priority = "5"
    else:
        priority = "3" #  NORMAL
    
    return priority

def send_email_gmail(from_address: str,
                     subject: str,
                     message: str,
                     priority: str,
                     to_address: list = [],
                     attach: list = []) -> None:
    smtp_server, smtp_port = get_smtp_server_and_port_gmail()  
    password: str = os.getenv("PasswordGmail")
    priority: str = get_priority_email(priority)
    
    text = MIMEText(message, "html")
    header = MIMEMultipart()
    
    # Caso tenha anexos
    if attach:
        for attach_in in attach:
            base = MIMEBase("application", "octet-stream") 
            base.set_payload(open(attach_in, "rb").read())
            encoders.encode_base64(base)
            attach_filename = os.path.split(attach_in)
            base.add_header("Content-Disposition", "attachment; filename="+str(attach_filename[1]))
            header.attach(base)
    
    header.attach(text)
    header["Subject"] = subject
    header["From"] = from_address
    header["To"] = ",".join(to_address)
    header["Date"] = formatdate(localtime=True)
    header["X-Priority"] = priority
    
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_address, password)
        smtp.sendmail(from_address, to_address, header.as_string())
        smtp.quit()
        print_message("Email enviado com sucesso", "OK")
    except Exception as error_email:
        print_message(f"Falha ao enviar email. Erro: {error_email}", "W")
            
def get_location_teste_azv(environment: str) -> str:
    smtp_server = "172.205.3.181"
    
    if environment == "CI": #  CI
        smtp_server = "172.200.48.95" #  AZV CI (DW011VW-CI-AZV)
    elif environment == "DM": #  DEMO
        smtp_server = "172.200.48.95" #  AZV DEMO
    elif environment == "QD": #  QED
        smtp_server = "172.200.179.81" #  AZV QED
    
    return smtp_server

def get_smtp_server_and_port() -> tuple(str, str):
    smtp_server = "smtpdc.dominiosistemas.com.br"
    smtp_port = 25
    
    if LOCATION == "LCW":
        smtp_server = "smtpdc.dominiosistemas.com.br"
    elif LOCATION == "SKY":
        smtp_server = "smtp01.dominioweb.local"
    elif LOCATION == "AZV":
        smtp_port = 587
        smtp_server = get_location_teste_azv(ENVIRONMENT)
    else:
        smtp_server = "smtpdc.dominiosistemas.com.br"
    
    return smtp_server, smtp_port

def send_email(from_address: str,
              subject: str,
              message: str,
              priority: str,
              to_address: list = [],
              attach: list = []):
    smtp_server, smtp_port = get_smtp_server_and_port()  
    
    text = MIMEText(message, "html")
    header = MIMEMultipart()
    
    # Caso tenha anexos
    if attach:
        for attach_in in attach:
            base = MIMEBase("application", "octet-stream") 
            base.set_payload(open(attach_in, "rb").read())
            encoders.encode_base64(base)
            attach_filename = os.path.split(attach_in)
            base.add_header("Content-Disposition", "attachment; filename="+str(attach_filename[1]))
            header.attach(base)
    
    header.attach(text)
    header["Subject"] = subject
    header["From"] = from_address
    header["To"] = ",".join(to_address)
    header["Date"] = formatdate(localtime=True)
    header["X-Priority"] = get_priority_email(priority)
    
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.sendmail(from_address, to_address, header.as_string())
        smtp.quit()
        print_message("Email enviado com sucesso", "OK")
    except Exception as error_email:
        print_message(f"Falha ao enviar email. Erro: {error_email}", "W")

def SendEmailInfo(subject: str,
                  message: str,
                  priority: str,
                  to_address: list = [],
                  attach: list = []):
    subject = HOSTNAME + "::" + SCRIPT_FRIENDLYNAME + "::" + subject
    from_address = "ListIncludedClientsWithgroups.Info <listincludedclientswithgroups.info@dominiosistemas.com.br>"
    
    send_email(from_address = from_address, 
              subject = subject, 
              message = message, 
              priority = priority, 
              to_address = to_address,
              attach = attach)

def SendEmailWarnig(subject: str,
                  message: str,
                  priority: str,
                  to_address: list = [],
                  attach: list = []):
    subject = HOSTNAME + "::" + SCRIPT_FRIENDLYNAME + "::" + subject
    from_address = "ListIncludedClientsWithEngine.Warning <listincludedclientswithengine.warning@dominiosistemas.com.br>"
    
    send_email(from_address = from_address, 
              subject = subject, 
              message = message, 
              priority = priority, 
              to_address = to_address,
              attach = attach)

def SendEmailError(subject: str,
                  message: str,
                  priority: str,
                  to_address: list = [],
                  attach: list = []):
    subject = HOSTNAME + "::" + SCRIPT_FRIENDLYNAME + "::" + subject
    from_address = "ListIncludedClientsWithEngine.Error <listincludedclientswithengine.error@dominiosistemas.com.br>"
    
    send_email(from_address = from_address, 
              subject = subject, 
              message = message, 
              priority = priority, 
              to_address = to_address,
              attach = attach)
