import smtplib

from email.message import EmailMessage

#Parte V - Enviando o relatório via e-mail

def enviar_email(remetente, senha, lista_email, mensagem):

    if lista_email:
        emails = lista_email.split(",")

        for email in emails:
            print(f"Enviando para: {email}")
    else:
        print("A variável EMAIL_LIST não foi definida no arquivo .env.")

    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = remetente
    msg['To'] = lista_email
    msg.set_content(mensagem)

    try:
        with open("data/citacoes.csv", "rb") as f:
            msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="citacoes.csv")
    except FileNotFoundError:
        print("Erro! Arquivo csv não encontrado.")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
            print("\nE-mail enviado com sucesso! CONCLUIDO!!!")
    except Exception as e:
        print(f"Falha ao enviar e-mail! \n {e}")

    return {
        "status": "E-mail enviado com sucesso",
        "destinatarios": lista_email
    }
