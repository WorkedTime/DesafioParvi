import os

import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

from src.processando_dados import processando_dados

#Parte IV - Enviando o relatório via e-mail
load_dotenv(override=True)

def enviar_email():

    total = data("quotes")
    citacoes = (total["Citacoes"])
    autor = (total["Autor"])
    tags = (total["Tag"])

    user = os.getenv("EMAIL")
    password = os.getenv("PASS")
    email_list = os.getenv("EMAIL_LIST")

    if email_list:
        emails = email_list.split(",")

        for email in emails:
            print(f"Sucesso! Enviado para: {email}")
    else:
        print("A variável EMAIL_LIST não foi definida no arquivo .env.")

    if not user or not password:
        print("Erro: EMAIL ou PASS não estão definidos no .env")
        return

    #Envio de e-mail sendo remetente, destinatário e corpo da mensagem definidos
    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = user
    msg['To'] = email_list
    msg.set_content(f"Arquivos gerados do CSV:\n Total de {citacoes} Citações\n O autor mais recorrente é: {autor}\n A tag mais utilizada é: {tags}")

    try:
        with open("data/citacoes.csv", "rb") as f:
            msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="citacoes.csv")
    except FileNotFoundError:
        print("Erro! Arquivo csv não encontrado.")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
            print("\nE-mail enviado com sucesso! CONCLUIDO!!!")
    except Exception as e:
        print(f"Falha ao enviar e-mail! \n {e}")
    return {
        "status": "E-mail enviado com sucesso",
        "destinatarios": email_list
    }
