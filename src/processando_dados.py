import ast
import pandas as pd

#Part II - Lendo arquivo CSV pós criado e tornando em lista literal

#1.Lê o arquivo(csv) e filtra por contagem(value_counts), maior repetição(idxmax), por lista(ast.literal_eval), por palavras inteiras(ast.literal_eval) e coloca como upper a primeira letra das palavras listadas no arquivo(csv) criado  
#2.Imprime para o usuário o autor e tag mais frequentes dentro do arquivo(csv) gerado

def processando_dados() -> dict:

    df = pd.read_csv("data/citacoes.csv") #Determina que o DataFrame do Pandas busque e leia o arquivo csv gerado acima

    total_quotes = df["Texto"].value_counts().count() #Lê os dados da coluna "Texto" no DataFrame e conta cada uma delas na lista
    print(f"\nQuantidade total de citações: {total_quotes}") #Mostra a contagem de citações/textos

    autor_mais_frequente = df["Autor"].value_counts().idxmax() #Lê os dados na coluna "Autor" no DataFrame e conta cada valor separadamente e também guarda o mais repetido
    print(f"Autor mais recorrente: {autor_mais_frequente}") #Mostra o resultado pós filtro do dado final

    tag_mais_frequente = df["Tags"].apply(ast.literal_eval).explode().str.capitalize().value_counts().idxmax() #Lê os dados na coluna "Tags " do DataFrame e aplica a cada coluna uma forma segura de ler os dados como uma lista ou dicionário validando-os, depois os separa e lê cada uma das palavras armazenadas, além de deixar a primeira letra de cada palavra impressa maiúscula e fazendo sua contagem, revelando também a tag mais repetida
    print(f"Tag mais utilizada: {tag_mais_frequente}\n") #Mostra o resultado pós filtro acima do dado final

    return { #Usado para retornar os dados filtrados e processados para serem usados posteriormente
    'Citacoes':int(total_quotes),
    'Autor':autor_mais_frequente,
    'Tag':tag_mais_frequente
    }
