from src.processando_dados import processando_dados
from src.enviar_email import enviar_email
from src.encontrando_dados import encontrando_dados
from src.criando_csv import criando_csv
from dotenv import load_dotenv

load_dotenv(Override=True)

user = os.getenv("EMAIL")
password = os.getenv("PASS")

user_thiago = os.getenv("EMAIL")
password_thiago = os.getenv("PASS")

email_list = os.getenv("EMAIL_LIST")

def main():         

    #Parte I - Busca de dados via URL e filtro de buscas
    dicionario_quotes = encontrando_dados()

    #Parte II - Criando arquivo csv com os dados gerados
    criando_csv(dicionario_quotes)

    #Parte III - Lendo arquivo CSV pós criado e tornando em lista literal
    processando_dados()

    #Parte IV - Enviando o relatório via e-mail
    enviar_email(rementeeee=user, password, email_list)
    enviar_email(remetente=user_thiago, senha=password_thiago, lista_email=email_list)

if __name__ == "__main__":
    main() 
