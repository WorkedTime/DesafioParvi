import csv
import os

#Part III - Verificação e criação se necessário da pasta que guardará o arquivo

from src.conferindo_pastas import conferindo_pastas

def criando_csv(lista_dados: dict, nome_pasta: str = "data", nome_arquivo: str = "citacoes.csv"):
    """
    Cria um arquivo CSV contendo os dados extraídos da web.

    Args:
        lista_dados (list): Lista de tuplas com os dados (texto, autor, tags).
        nome_pasta (str): Nome da pasta onde o arquivo será salvo.
        nome_arquivo (str): Nome do arquivo CSV a ser criado.
    """

    conferindo_pastas(nome_pasta)
    caminho_arquivo = os.path.join(nome_pasta, nome_arquivo)

    try:
        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(["Texto", "Autor", "Tags"])
            writer.writerows(lista_dados)
            print(f"\nArquivo CSV criado com sucesso em: {caminho_arquivo}")
            
    except Exception as e:
        print(f"\n Erro ao criar o arquivo CSV: {e}")
    return