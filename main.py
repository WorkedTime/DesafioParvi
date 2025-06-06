import os

from dotenv import load_dotenv

from src.encontrando_dados import encontrando_dados #Part I
from src.conferindo_pastas import conferindo_pastas #Part II
from src.criando_csv import criando_csv #Part III
from src.processando_dados import processando_dados #Part IV
from src.corpo_email import msg_corpo_email #Part V
from src.enviar_email import enviar_email #Part VI

load_dotenv(override=True)

user = os.getenv("EMAIL")
password = os.getenv("PASS")

email_list = os.getenv("EMAIL_LIST")

def main():
    # Part I - Busca de dados via URL e filtro de buscas
    resultado = encontrando_dados()
    lista_citacoes = resultado["quotes"]
    # Part II - Conferência de pasta
    nome_pasta = conferindo_pastas()
    #Part III - Criação do CSV
    nome_arquivo = "citacoes.csv"
    criando_csv(lista_citacoes, nome_pasta=nome_pasta, nome_arquivo=nome_arquivo)
    # Part IV - Processamento de dados a partir do CSV
    lista_dados = processando_dados(nome_pasta=nome_pasta, nome_arquivo=nome_arquivo)
    # Part V - Criação da mensagem do e-mail
    corpo_mensagem = msg_corpo_email(lista_dados)
    # Part VI - Envio do e-mail
    caminho_csv = os.path.join(nome_pasta, nome_arquivo)
    enviar_email(user,password,email_list, corpo_mensagem, caminho_csv)

if __name__ == "__main__":
    main() 
