import os

import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from processando_dados import processando_dados

#Parte III - Enviando o relatório via e-mail (Extra)
load_dotenv()

#1.Estabele o envio de dados(csv) para os destinatários inclusos no (.env) por meio de senha gerada pela google para a plataforma de envio e corpo de e-mail definido para se evitar erros
#2.Envio de aviso caso o arquivo (csv) não seja encontrado

def enviar_email():

    total = processando_dados() #Uso da função processando_dados para obter os dados filtrados e processados
    citacoes = (total["Citacoes"])
    autor = (total["Autor"])
    tags = (total["Tag"])

    user = os.getenv("EMAIL") #Obtém o e-mail do remetente a partir do arquivo .env
    password = os.getenv("PASS") #Obtém a senha do remetente a partir do arquivo .env
    email_list = os.getenv("EMAIL_LIST") #Obtém a lista de e-mails do destinatário a partir do arquivo .env

    if email_list: #Verifica se a variável está definida
        emails = email_list.split(",") #Cria a lista de e-mails usando o delimitador (vírgula neste caso)

        for email in emails: #Remove espaços em branco desnecessários
            print(f"Sucesso! Enviado para: {email}") #Exibe a lista de e-mails que receberão o relatório
    else:
        print("A variável EMAIL_LIST não foi definida no arquivo .env.") #Exibe mensagem de erro caso a variável não esteja definida

    if not user or not password:
        print("Erro: EMAIL ou PASS não estão definidos no .env") #Exibe mensagem de erro caso o e-mail ou a senha não estejam definidos no arquivo .env
        return

    #Envio de e-mail sendo remetente, destinatário e corpo da mensagem definidos
    msg = EmailMessage() #Cria uma mensagem de e-mail
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = user
    msg['To'] = email_list
    msg.set_content(f"Arquivos gerados do CSV:\n Total de {citacoes} Citações\n O autor mais recorrente é: {autor}\n A tag mais utilizada é: {tags}") #Define o conteúdo do e-mail com os dados filtrados

    try:
        with open("data/citacoes.csv", "rb") as f: #Abre o arquivo csv em modo leitura binária
            msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="citacoes.csv") #Adiciona o arquivo como anexo à mensagem de e-mail
    except FileNotFoundError:
        print("Erro! Arquivo csv não encontrado.") #Exibe mensagem de erro caso o arquivo csv não seja encontrado
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: #Cria uma conexão segura com o servidor SMTP do Gmail
            smtp.login(user, password) #Faz login no servidor SMTP usando o e-mail e a senha
            smtp.send_message(msg) #Envia a mensagem de e-mail
            print("\nE-mail enviado com sucesso!")
    except Exception as e: #Exceção para capturar erros durante o envio do e-mail
        print(f"Falha ao enviar e-mail! \n {e}")
