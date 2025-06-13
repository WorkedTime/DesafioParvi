import csv
import os

#Part III - Verificação e criação se necessário da pasta que guardará o arquivo

from src.conferindo_pastas import conferindo_pastas
#Organizar o busca_1 busca_2 e busca_3 - TODOS
#Refazer as DOCSTRINGS - TODOS

def criando_csv(lista_dados: dict, nome_pasta: str = "data", nome_arquivo: str = "citacoes.csv", busca_1: str = "Texto", busca_2: str = "Autor", busca_3: str = "Tags"):
    """
    Cria um arquivo CSV contendo os dados extraídos da web.

    Args:
        lista_dados (dict): Valores armazenados em um dicionário com os dados (texto, autor, tags).
        nome_pasta (str): Nome da pasta onde o arquivo será salvo.
        nome_arquivo (str): Nome do arquivo CSV a ser criado.
        busca_1 (str): 1ª busca por dados escolhidos pelo usuário
        busca_2 (str): 2ª busca por dados escolhidos pelo usuário
        busca_3 (str): 3ª busca por dados escolhidos pelo usuário
    """

    conferindo_pastas(nome_pasta)
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)

    try:
        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow([busca_1, busca_2, busca_3])
            writer.writerows(lista_dados)
            print(f"\nArquivo CSV criado com sucesso em: {caminho_arquivo}")
            
    except Exception as e:
        print(f"\n Erro ao criar o arquivo CSV: {e}")
