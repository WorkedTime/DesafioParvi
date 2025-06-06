import os

#Part II - Confere e cria pastas caso não sejam encontradas
def conferindo_pastas(caminho_pasta: str ="data") -> str:

    try:
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
            print(f"\nDiretório '{caminho_pasta}' criado com sucesso!")
        else:
            print(f"\nArquivo {caminho_pasta} já existe!")
            return
    except Exception as e:
        print(f"\nErro ao criar o diretório '{caminho_pasta}': {e}")
        return 
    