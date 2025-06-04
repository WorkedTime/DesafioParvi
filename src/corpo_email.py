from selenium.webdriver.support import expected_conditions as EC
from src.processando_dados import processando_dados

#Part IV - Caso aja alteração do corpo do texto

def msg_corpo_email(total_dicionario):
    
    #Mensagem do corpo do e-mail
    try:
        mensagem = f"Olá, seguem os dados após análise de conteúdo visto via Web e processado via Pandas:\n\n\nO Total de citações é de {total_dicionario["Citacoes"]} Citações \nO autor mais recorrente é o: {total_dicionario["Autor"]}\nE a tag mais repetida é a: {total_dicionario["Tag"]}"

    except (NameError, SyntaxError, UnicodeError):
        print("\nNavegação finalizada por erro em sintaxe ou os elementos solicitados não são compativeis com o arquivo!")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        raise RuntimeError("\nErro de execução!") from e
    
    return mensagem
