import ast
import os

import pandas as pd

#Parte IV - Processamento de dados pós buscas junto ao CSV

def processando_dados(nome_pasta: str ="data", nome_arquivo: str ="citacoes.csv", busca_1: str = "Texto", busca_2: str = "Autor", busca_3: str = "Tags") -> dict:
    """
    Processa os dados do CSV, identificando:
    - Total de citações
    - Autor mais recorrente
    - Tag mais usada

    Args:
        nome_pasta (str): Nome da pasta onde está o CSV.
        nome_arquivo (str): Nome do arquivo CSV a ser lido.
        busca_1 (str): 1ª busca por dados escolhidos pelo usuário
        busca_2 (str): 2ª busca por dados escolhidos pelo usuário
        busca_3 (str): 3ª busca por dados escolhidos pelo usuário

    Returns:
        dict: Dicionário com os dados filtrados ('Citacoes', 'Autor', 'Tag').
    """

    try:
        df = pd.read_csv(os.path.join(nome_pasta, nome_arquivo))

        total_quotes = df[busca_1].value_counts().count()
        print(f"\nQuantidade total de citações: {total_quotes}") 

        autor_mais_frequente = df[busca_2].value_counts().idxmax()
        print(f"Autor mais recorrente: {autor_mais_frequente}")

        tag_mais_frequente = (df[busca_3].apply(ast.literal_eval).explode().str.capitalize().value_counts().idxmax())
        print(f"Tag mais utilizada: {tag_mais_frequente}\n")

    except FileNotFoundError:
        print("\nErro! Arquivo CSV não encontrado.")
        raise FileNotFoundError("\nO arquivo CSV não pode ser encontrado no caminho especificado")
        
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        raise RuntimeError("\nErro de execução!") from e
    
    total_dicionario = {
        "Citacoes": int(total_quotes),
        "Autor": autor_mais_frequente,
        "Tag": tag_mais_frequente,
        }

    return total_dicionario
