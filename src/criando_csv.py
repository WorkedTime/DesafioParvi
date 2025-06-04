import csv
import os

from src.encontrando_dados import encontrando_dados
from src.conferindo_pastas  import conferindo_pastas

# Part III - Criação de CSV pós buscas na Web

def criando_csv(lista_dados, pasta, arquivo):

    total_lista = lista_dados["quotes"]

    try:
        with open(arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(["Texto", "Autor", "Tags"])
            writer.writerows(total_lista)
            print(f"\nArquivo CSV criado com sucesso dentro da pasta {pasta}!")

    except Exception as e:
        print(f"\nErro ao criar o arquivo CSV: {e}")

    return {
        "status": "CSV criado com sucesso",
        "caminho": arquivo
    }
