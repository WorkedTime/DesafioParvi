import csv
import os
from src.encontrando_dados import encontrando_dados

# Part II - Criação de CSV pós buscas na Web

def criando_csv():
    pasta = "data"
    arquivo = os.path.join(pasta, "citacoes.csv")

    #Verifica e cria a pasta se necessário
    if not os.path.exists(pasta):
        try:
            os.mkdir(pasta)
            print(f"\nDiretório {pasta} criado com sucesso!")
        except Exception as e:
            print(f"\nErro ao criar o diretório {pasta}: {e}")
            return
    else:
        print(f"\nDiretório {pasta} já existe.")

        total_lista = total_dados("quotes")

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
