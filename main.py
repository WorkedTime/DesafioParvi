from src.processando_dados import processando_dados
from src.enviar_email import enviar_email
from src.encontrando_dados import encontrando_dados
from src.criando_csv import criando_csv

def main():         

    #Parte I - Busca de dados via URL e filtro de buscas
    encontrando_dados()

    #Parte II - Criando arquivo csv com os dados gerados
    criando_csv()

    #Parte III - Lendo arquivo CSV pós criado e tornando em lista literal
    processando_dados()

    #Parte IV - Enviando o relatório via e-mail
    enviar_email()

if __name__ == "__main__":
    main() 
