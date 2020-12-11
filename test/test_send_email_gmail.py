# encoding: utf-8

import pytest
from framework.my_email import send_email_gmail

from_email = []

@pytest.mark.parametrize("from_email", from_email)
def test_send_email_gmail(from_email):
    to_address = []
    subject = "Pytest - Teste de envio de e-mail"
    message = "Este e-mail está sendo enviado apenas como teste."
    
    send_email_gmail(from_address = from_email, 
                     subject = subject, 
                     message = message,
                     priority="3",
                     to_address = to_address,
                     attach=[]
                     )