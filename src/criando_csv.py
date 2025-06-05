import csv
import os

from src.conferindo_pastas import conferindo_pastas

def criando_csv(lista_dados, nome_pasta="data", nome_arquivo="citacoes.csv"):

    caminho_pasta = conferindo_pastas(nome_pasta)
    if not caminho_pasta:
        return {"status": "Erro na criação da pasta", "caminho": None}

    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

    try:
        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(["Texto", "Autor", "Tags"])
            writer.writerows(lista_dados)
            print(f"\n Arquivo CSV criado com sucesso em: {caminho_arquivo}")

        return {"status": "CSV criado com sucesso", "caminho": caminho_arquivo}

    except Exception as e:
        print(f"\n Erro ao criar o arquivo CSV: {e}")
        return {"status": "Erro ao criar CSV", "caminho": None}
    