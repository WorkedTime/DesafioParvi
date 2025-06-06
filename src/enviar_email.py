import smtplib

from email.message import EmailMessage

#Parte VI - Enviando o relatório via e-mail

def enviar_email(remetente: str, senha: str, lista_email: list, mensagem: str, nome_arquivo: str):
    """
    Envia um e-mail com os dados processados e o arquivo em anexo.

    Args:
        remetente (str): Endereço de e-mail do remetente.
        senha (str): Senha ou app-password do remetente.
        lista_email (list): Lista de destinatários separados por vírgula.
        mensagem (str): Corpo do e-mail.
        nome_arquivo (str): Caminho do arquivo CSV a ser anexado.

    Returns:
        dict: Dicionário com o status do envio e lista de destinatários.
    """

    emails = lista_email.split(",")
    if not emails:
        print("\nEmails não definidos no .env!")
        return
    for email in emails:
        print(f"Enviado com sucesso para: {email}!")

    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = remetente
    msg['To'] = ",".join(emails)
    msg.set_content(mensagem)

    try:
        with open(nome_arquivo, "rb") as f:
            msg.add_attachment(f.read(), maintype='text', subtype='csv', filename="citacoes.csv")
    except FileNotFoundError:
        print("Erro! Arquivo csv não encontrado.")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
            print("\nTodas as etapas aprovadas! CONCLUIDO!!!")
    except Exception as e:
        print(f"Falha ao enviar e-mail! \n {e}")

    return {
        "status": "E-mail enviado com sucesso",
        "destinatarios": lista_email
    }
