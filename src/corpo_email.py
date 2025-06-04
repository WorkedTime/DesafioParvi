from src.processando_dados import processando_dados

def msg_corpo_email(total_dicionario):
    
    #Mensagem do corpo do e-mail
    mensagem = f"Olá, seguem os dados após análise de conteúdo visto via Web e processado via Pandas:\n\n\nO Total de citações é de {total_dicionario["Citacoes"]} Citações \nO autor mais recorrente é o: {total_dicionario["Autor"]}\nE a tag mais repetida é a: {total_dicionario["Tag"]}"

    return mensagem
