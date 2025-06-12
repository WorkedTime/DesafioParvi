from src.processando_dados import processando_dados

#Part V - Caso aja alteração do corpo do texto

def msg_corpo_email(total_dicionario: dict, busca_1: str = "Citacoes", busca_2: str = "Autor", busca_3: str = "Tag") -> str:
    """
    Gera o corpo do e-mail a partir das informações processadas.

    Args:
        total_dicionario (dict): Dicionário com os dados de citações, autor e tag.
        busca_1 (str): 1ª busca por dados escolhidos pelo usuário
        busca_2 (str): 2ª busca por dados escolhidos pelo usuário
        busca_3 (str): 3ª busca por dados escolhidos pelo usuário
        
    Returns:
        str: Texto formatado para envio por e-mail.
    """

    #Mensagem do corpo do e-mail
    try:
        mensagem = f'Olá, seguem os dados após análise de conteúdo visto via Web e processado via Pandas:\n\n\nO Total de citações é de {total_dicionario[busca_1]} Citações \nO autor mais recorrente é o: {total_dicionario[busca_2]}\nE a tag mais repetida é a: {total_dicionario[busca_3]}'
    
    except (KeyError, UnicodeError):
        print("\nNavegação finalizada por erro em sintaxe ou os elementos solicitados não são compativeis com o arquivo!")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        raise RuntimeError("\nErro de execução!") from e

    return mensagem
