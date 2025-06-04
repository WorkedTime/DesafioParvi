import os
from src.corpo_email import msg_corpo_email
from src.processando_dados import processando_dados
from src.enviar_email import enviar_email
from src.encontrando_dados import encontrando_dados
from src.criando_csv import criando_csv
from dotenv import load_dotenv

load_dotenv(override=True)

user = os.getenv("EMAIL")
password = os.getenv("PASS")

email_list = os.getenv("EMAIL_LIST")

def main():

    #Parte I - Busca de dados via URL e filtro de buscas
    dicionario_quotes = encontrando_dados()

    #Parte II - Criando arquivo csv com os dados gerados
    criando_csv(dicionario_quotes)

    #Parte III - Lendo arquivo CSV pós criado e tornando em lista literal
    lista_dados = processando_dados()
    mensagem = msg_corpo_email(lista_dados)
    #Parte IV - Enviando o relatório via e-mail
    enviar_email(user, password, email_list, mensagem)

if __name__ == "__main__":
    main() 
