from src.processando_dados import processando_dados
from src.enviar_email import enviar_email
from src.encontrando_dados import encontrando_dados

def main():         

    #Parte I - Busca de dados via URL e filtro de buscas
    encontrando_dados()

    #Parte II - Lendo arquivo CSV pós criado e tornando em lista literal
    total = processando_dados()

    #Parte III - Enviando o relatório via e-mail
    enviar_email()

main() 
