import smtplib
from email.mime.text import MIMEText
import threading
from Usuario import settings
from random import *
import string

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    # Verifica se os dígitos calculados são iguais aos do CPF
    return cpf[-2:] == f"{digito1}{digito2}"

def enviar_email(subject,body,recipients):
        html_message = MIMEText(body, 'html')
        html_message['Subject'] = subject
        html_message['From'] = settings.EMAIL_HOST_USER
        html_message['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, recipients, html_message.as_string())   

def enviar_email_background(subject, body, recipients):
    def send():
        try:
            html_message = MIMEText(body, 'html')
            html_message['Subject'] = subject
            html_message['From'] = settings.EMAIL_HOST_USER
            html_message['To'] = ', '.join(recipients)
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER, recipients, html_message.as_string())
            return "Mensagem enviada com sucesso"
        except Exception as e:
            print(e)
            return e    

    # Cria e inicia a thread
    thread = threading.Thread(target=send)
    thread.start()


def gera_senha(tamanho):
    caracteres = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters
    senha = ''.join(choice(caracteres) for i in range(tamanho-1))
    senha=choice(string.ascii_uppercase)+senha
    return senha