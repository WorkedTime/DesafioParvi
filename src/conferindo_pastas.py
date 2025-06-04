import os

#Part II - Confere e cria pastas caso não sejam encontradas

def conferindo_pastas():

    pasta = 'data'
    arquivo = os.path.join(pasta, "")

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

        return pasta, arquivo
    
    #pasta no caminho atual 
    #arquivo recebendo string para o nome novo