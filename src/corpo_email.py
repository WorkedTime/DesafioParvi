from src.processando_dados import processando_dados

def msg_corpo_email(total_dicionario):
    
    mensagem = f"Mensagem do corpo do e-mail: O Total de citações é de {total_dicionario["Citacoes"]}\n O autor mais recorrente é o: {total_dicionario["Autor"]}\n E a tag mais repetida é a: {total_dicionario["Tag"]}"

    return mensagem
