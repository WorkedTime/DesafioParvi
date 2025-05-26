import csv
import os 

import ast
import pandas as pd
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

#Part I - Busca de dadps via URL e filtro de buscas

#1.Instalação do driver do Chrome, além de baixar a versão mais recente para a sua máquina, iniciando o navegador e se conectando ao Selenium.
#2.Acesso ao site com o driver.get e armazenando na lista quote_lists, executando o script em loop enquanto verdadeiro para encontro das citações por busca de elementos via name, também manusendo com uso de except para qualquer erro de busca.
#3.Click de botão next para permanência de buscas em outras páginas do mesmo site.
#4.Tratativa de erro caso a busca falhe, além de aviso e encerramento visível da função.
#5.Cria o arquivo (csv)
#6.Encerramento do Driver.   

def encontrando_dados():

    service = Service(ChromeDriverManager().install()) #Faz download ou encontra o ChromeDriver adequado a versã instalada no sistema
    driver = webdriver.Chrome(service=service) #ChromeDriver -> Service que inicializa o navegador Chrome e se conecta ao Selenium parmitindo as automações

    driver.get("https://quotes.toscrape.com/js-delayed/") #Acessa o site de busca de informações

    quotes_list = [] #Lista para armazenar as citações

    while True: #Executa enquanto o loop se mostrar verdadeiro
        try:

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))) #Aguarda até que as citações sejam carregadas

            #Coleta as citações na página atual
            quotes = driver.find_elements(By.CLASS_NAME, "quote") #Encontra elementos com o nome "quote"
            for quote in quotes: #Loop for para repetição de busca
                #texts = [texto.text for texto in quote.find_elements(By.CLASS_NAME, "text")] #Encontra elementos com o nome "text"
                texts = [texto.text for texto in quote.find_elements(By.CLASS_NAME, "text")]
                author = quote.find_element(By.CLASS_NAME, "author").text #Encontra elementos com o nome "author"
                tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
                quotes_list.append((texts, author, tags)) #Adiciona a lista as tabelas "tag", "text" e "author"
                print(f"{texts} - {author} - {tags}") #Mostra aquilo que está sendo encontrado nas tabelas de "text", "author" e "tag"

            #Tenta encontrar o botão "Next"
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.next > a') #Encontra e retorna um elemento <a>(link) que está dentro de um <li>(lista) com classe next(página ou item em lista)
            next_button.click() #Faz a página sucessora ser clicada

        except (NoSuchElementException, TimeoutException):  #Erros que podem gerar esgotamento de tempo e de nenhum elemento encontrado
            print("Navegação finalizada ou erro ao carregar a próxima página.") #Aviso sobra a detecção de erro
            break #Da parada a função independente do que aconteça

    driver.quit() #Encerramento de Driver

    print(f"\nTotal de citações coletadas: {len(quotes_list)}") #Exibe o total de citações extraídas

    with open("data/citacoes.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv: # with open forma de abrir e fechar arquivo de forma segura mesmo que ocorra erro | 'w' abre o arquivo no modo escrita e sobrescreve ou cria um novo | newline exita linhas em brancos extras | utf-8 define a codificação garantindo acentuação e caracteres especiais | as arquivo_csv representa o objeto do arquivo aberto
        writer = csv.writer(arquivo_csv) #Função csv que cria um objeto gravador para escrita de dados | arquivo_csv é onde sera armazenado os dados | escreve linhas no arquivo csv 
        writer.writerow(["Texto", "Autor", "Tags"]) #Cabeçalhos do arquivo.csv
        writer.writerows(quotes_list) #Escreve as linhas recebidas do arquivo gerado pela lista de busca

    print("\nArquivo csv gerado com sucesso!")

encontrando_dados()

#Part II - Lendo arquivo CSV pós criado e tornando em lista literal

#1.Lê o arquivo(csv) e filtra por contagem(value_counts), maior repetição(idxmax), por lista(ast.literal_eval), por palavras inteiras(ast.literal_eval) e coloca como upper a primeira letra das palavras listadas no arquivo(csv) criado  
#2.Imprime para o usuário o autor e tag mais frequentes dentro do arquivo(csv) gerado

def processando_dados():

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


#Parte III - Enviando o relatório via e-mail (Extra)
load_dotenv()

#1.Estabele o envio de dados(csv) para os destinatários inclusos no (.env) por meio de senha gerada pela google para a plataforma de envio e corpo de e-mail definido para se evitar erros
#2.Envio de aviso caso o arquivo (csv) não seja encontrado

def enviar_email():

    total = processando_dados() #Uso da função processando_dados para obter os dados filtrados e processados
    citacoes = (total["Citacoes"])
    autor = (total["Autor"])
    tags = (total["Tag"])

    user = os.getenv("EMAIL") #Obtém o e-mail do remetente a partir do arquivo .env
    password = os.getenv("PASS") #Obtém a senha do remetente a partir do arquivo .env
    email_list = os.getenv("EMAIL_LIST") #Obtém a lista de e-mails do destinatário a partir do arquivo .env

    if email_list: #Verifica se a variável está definida
        emails = email_list.split(",") #Cria a lista de e-mails usando o delimitador (vírgula neste caso)
        print(emails)

        for email in emails: #Remove espaços em branco desnecessários
            print(f"Sucesso! Enviado para: {email}") #Exibe a lista de e-mails que receberão o relatório
            print(email)
    else:
        print("A variável EMAIL_LIST não foi definida no arquivo .env.") #Exibe mensagem de erro caso a variável não esteja definida

    if not user or not password:
        print("Erro: EMAIL ou PASS não estão definidos no .env") #Exibe mensagem de erro caso o e-mail ou a senha não estejam definidos no arquivo .env
        return

    #Envio de e-mail sendo remetente, destinatário e corpo da mensagem definidos
    msg = EmailMessage() #Cria uma mensagem de e-mail
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = user
    msg['To'] = email_list
    msg.set_content(f"Os dados gerados do arquivo csv são: {citacoes} Citações\n O autor mais recorrente é: {autor}\n A tag mais utilizada é: {tags}") #Define o conteúdo do e-mail com os dados filtrados

    try:
        with open("data/citacoes.csv", "rb") as f: #Abre o arquivo csv em modo leitura binária
            msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="citacoes.csv") #Adiciona o arquivo como anexo à mensagem de e-mail
    except FileNotFoundError:
        print("Erro! Arquivo csv não encontrado.") #Exibe mensagem de erro caso o arquivo csv não seja encontrado
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: #Cria uma conexão segura com o servidor SMTP do Gmail
            smtp.login(user, password) #Faz login no servidor SMTP usando o e-mail e a senha
            smtp.send_message(msg) #Envia a mensagem de e-mail
            print("\nE-mail enviado com sucesso!")
    except Exception as e: #Exceção para capturar erros durante o envio do e-mail
        print(f"Falha ao enviar e-mail! \n {e}")

enviar_email()
