import csv
import os

#Part IV

from src.conferindo_pastas import conferindo_pastas

def criando_csv(lista_dados: dict, nome_pasta: str = "data", nome_arquivo: str = "citacoes.csv"):

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