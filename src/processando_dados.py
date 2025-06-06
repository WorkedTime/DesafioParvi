import ast
import os

import pandas as pd

#Parte IV - Processamento de dados pós buscas junto ao CSV

def processando_dados(nome_pasta="data", nome_arquivo="citacoes.csv") -> dict:
    """
    Processa os dados do CSV, identificando:
    - Total de citações
    - Autor mais recorrente
    - Tag mais usada

    Args:
        nome_pasta (str): Nome da pasta onde está o CSV.
        nome_arquivo (str): Nome do arquivo CSV a ser lido.

    Returns:
        dict: Dicionário com os dados filtrados ('Citacoes', 'Autor', 'Tag').
    """

    try:
        df = pd.read_csv(os.path.join(nome_pasta, nome_arquivo))

        total_quotes = df["Texto"].value_counts().count()
        print(f"\nQuantidade total de citações: {total_quotes}") 

        autor_mais_frequente = df["Autor"].value_counts().idxmax()
        print(f"Autor mais recorrente: {autor_mais_frequente}")

        tag_mais_frequente = (df["Tags"].apply(ast.literal_eval).explode().str.capitalize().value_counts().idxmax())
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
