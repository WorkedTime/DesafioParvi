# **Desafio - RPA Python - Grupo Parvi**

Etapas do Desafio

1. **Web Scraping com Selenium**
2. **Processamento de Dados com Pandas**
3. **Envio de Relatório por E-mail**

## **Passo 1: Configurando o Ambiente de Desenvolvimento**

### **1.1 Instalei o python**

Via site: https://www.python.org/
Baixei a versão 3.13.3

### **1.2 Configurei o VS Code**

Realizei a instalação do `pip` no terminal:

```bash
python -m ensurepip --default-pip
```

Verifiquei a instalação e a versão:

```bash
pip --version
```

### **1.3 Criei um Ambiente Virtual**

Dentro do diretório do projeto, abri um terminal e executei o seguinte comando (é necessario o venv para executar o projeto):

```bash
python -m venv venv
```

Ativei o ambiente:

```bash
  venv\Scripts\activate
  pip install -r requeriments.txt
```

### **1.4 Instalei as Dependências**

Instalei as bibliotecas utiizando os seguintes comandos:

```bash
pip install selenium pandas python-dotenv webdriver-manager
```

Gerei o arquivo `requeriments.txt`:

```bash
pip freeze > requeriments.txt
```

## **Passo 2: Estruturei o Projeto**

Criei a seguinte estrutura de diretórios para deixar o projeto mais organizado:

```
📂 DESAFIOPARVI_1.1
 ┣ 📂 _pycache_         	# Arquivos compilados de módulos
 ┣ 📂 data              	# Pasta armazenando o arquivo CSV que foi gerado
    ┣ 📜 citacoes.csv      		# Armazenamento gerado dos arquivos de busca no CSV (Dentro da pasta data)
 ┣ 📂 src               	# Funções guardadas que serão chamadas pela main   
    ┣ 📂 _pycache_         	# Arquivos compilados de módulos
    ┣ 📜 encontrando_dados.py  		# Função criada para busca de dados via Web e criação do CSV
    ┣ 📜 processar_dados.py		# Função criada para envio dos dados pós filtros e finalização de contagens para os e-mails cadastrados na lista do arquivo .env
    ┣ 📜 enviar_email.py		# Função criada para leitura e novo filtro de dados do CSV, além da criação do return {} para uso em outra função
 ┣ 📂 venv              	# Ambiente virtual - Oculto
 ┣ 📜 .env              	# Credenciais para envio de e-mail - Oculto
 ┣ 📜 .env.examples     	# Credenciais não reais para exemplo de e-mail para o git  
 ┣ 📜 .gitignore        	# Biblioteca git para não uso de dados sensíveis dos usuários e desenvolvedor
 ┣ 📜 main.py           	# Arquivo principal do projeto
 ┣ 📜 README.md         	# Instruções do projeto
 ┣ 📜 requirements.txt  	# Dependências

```

## **Passo 3: Implementei Web Scraping com Selenium**

Criei uma função chamada encontrando_dados(): para envio dos arquivos buscados via automação e criação do arquivo CSV pós filtro para futuro uso na  `main.py` e adicione todos os imports e suas referências para busca dos dados:


import os

import csv

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from webdriver_manager.chrome import ChromeDriverManager


#Part I - Busca de dadps via URL e filtro de buscas


def encontrando_dados():

    service = Service(ChromeDriverManager().install()) #Faz download ou encontra o ChromeDriver adequado a versã instalada no sistema
    driver = webdriver.Chrome(service=service) #ChromeDriver -> Service que inicializa o navegador Chrome e se conecta ao Selenium parmitindo as automações

    busca = os.getenv("URL") #Obtém a URL do site a partir do arquivo .env
    driver.get(busca) #Acessa o site de busca de informações

    quotes_list = [] #Lista para armazenar as citações

    while True: #Executa enquanto o loop se mostrar verdadeiro
        try:

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))) #Aguarda até que as citações sejam carregadas

    #Coleta as citações na página atual
            quotes = driver.find_elements(By.CLASS_NAME, "quote") #Encontra elementos com o nome "quote"
            for quote in quotes: #Loop for para repetição de busca
                texts = [texto.text for texto in quote.find_elements(By.CLASS_NAME, "text")]
                author = quote.find_element(By.CLASS_NAME, "author").text #Encontra elementos com o nome "author"
                tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
                quotes_list.append((texts, author, tags)) #Adiciona a lista as tabelas "tag", "text" e "author"
                print(f"{texts} - {author} - {tags}") #Mostra aquilo que está sendo encontrado nas tabelas de "text", "author" e "tag"

    #Tenta encontrar o botão "Next"
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.next > a') #Encontra e retorna um elemento`<a>`(link) que está dentro de um `<li>`(lista) com classe next(página ou item em lista)
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


## **Passo 4: Realizei a leitura dos dados com o Pandas**

Criei uma função chamada processando_dados(): para filtro dos arquivos buscados via automação e pela leitura do arquivo CSV para chamada na  `main.py` e adicione todos os imports e suas referências para filtro destes dados e uso mais tarde:


import ast

import pandas as pd


#Part II - Lendo arquivo CSV pós criado e tornando em lista literal


defprocessando_dados() -> dict:

    df=pd.read_csv("data/citacoes.csv") #Determina que o DataFrame do Pandas busque e leia o arquivo csv gerado acima

    total_quotes=df["Texto"].value_counts().count() #Lê os dados da coluna "Texto" no DataFrame e conta cada uma delas na lista

    print(f"\nQuantidade total de citações: {total_quotes}") #Mostra a contagem de citações/textos

    autor_mais_frequente=df["Autor"].value_counts().idxmax() #Lê os dados na coluna "Autor" no DataFrame e conta cada valor separadamente e também guarda o mais repetido

    print(f"Autor mais recorrente: {autor_mais_frequente}") #Mostra o resultado pós filtro do dado final

    tag_mais_frequente=df["Tags"].apply(ast.literal_eval).explode().str.capitalize().value_counts().idxmax() #Lê os dados na coluna "Tags " do DataFrame e aplica a cada coluna uma forma segura de ler os dados como uma lista ou dicionário validando-os, depois os separa e lê cada uma das palavras armazenadas, além de deixar a primeira letra de cada palavra impressa maiúscula e fazendo sua contagem, revelando também a tag mais repetida

    print(f"Tag mais utilizada: {tag_mais_frequente}\n") #Mostra o resultado pós filtro acima do dado final

    return { #Usado para retornar os dados filtrados e processados para serem usados posteriormente

    'Citacoes':int(total_quotes),

    'Autor':autor_mais_frequente,

    'Tag':tag_mais_frequente

    }


## **Passo 5: Envio de dados via e-mail pelo smtplib**

Criei uma função chamada enviar_email(): para envio dos arquivos buscados via e-mail também chamada na  `main.py`  adicione todos os imports e suas referências para enviar apenas dados específicos no corpo(body) do e-mail:


import os

import smtplib

from dotenv import load_dotenv

from email.message import EmailMessage

from src.processando_dados import processando_dados


#Parte III - Enviando o relatório via e-mail


load_dotenv()


defenviar_email():

    total=processando_dados() #Uso da função processando_dados para obter os dados filtrados e processados

    citacoes= (total["Citacoes"])

    autor= (total["Autor"])

    tags= (total["Tag"])

    user=os.getenv("EMAIL") #Obtém o e-mail do remetente a partir do arquivo .env

    password=os.getenv("PASS") #Obtém a senha do remetente a partir do arquivo .env

    email_list=os.getenv("EMAIL_LIST") #Obtém a lista de e-mails do destinatário a partir do arquivo .env

    ifemail_list: #Verifica se a variável está definida

    emails=email_list.split(",") #Cria a lista de e-mails usando o delimitador (vírgula neste caso)

    foremailinemails: #Remove espaços em branco desnecessários

    print(f"Sucesso! Enviado para: {email}") #Exibe a lista de e-mails que receberão o relatório

    else:

    print("A variável EMAIL_LIST não foi definida no arquivo .env.") #Exibe mensagem de erro caso a variável não esteja definida

    ifnotuserornotpassword:

    print("Erro: EMAIL ou PASS não estão definidos no .env") #Exibe mensagem de erro caso o e-mail ou a senha não estejam definidos no arquivo .env

    return

    #Envio de e-mail sendo remetente, destinatário e corpo da mensagem definidos

    msg=EmailMessage() #Cria uma mensagem de e-mail

    msg['Subject'] ='Relatório de Citações'

    msg['From'] =user

    msg['To'] =email_list

    msg.set_content(f"Arquivos gerados do CSV:\n Total de {citacoes} Citações\n O autor mais recorrente é: {autor}\n A tag mais utilizada é: {tags}") #Define o conteúdo do e-mail com os dados filtrados

    try:

    withopen("data/citacoes.csv", "rb") asf: #Abre o arquivo csv em modo leitura binária

    msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="citacoes.csv") #Adiciona o arquivo como anexo à mensagem de e-mail

    exceptFileNotFoundError:

    print("Erro! Arquivo csv não encontrado.") #Exibe mensagem de erro caso o arquivo csv não seja encontrado

    return

    try:

    withsmtplib.SMTP_SSL('smtp.gmail.com', 465) assmtp: #Cria uma conexão segura com o servidor SMTP do Gmail

    smtp.login(user, password) #Faz login no servidor SMTP usando o e-mail e a senha

    smtp.send_message(msg) #Envia a mensagem de e-mail

    print("\nE-mail enviado com sucesso!")

    exceptExceptionase: #Exceção para capturar erros durante o envio do e-mail

    print(f"Falha ao enviar e-mail! \n{e}")


## **Passo 6: Após finalizar todo o andamento do projeto, versionei ele no meu git**

Realizei a insalação e configuração do git na minha maquina
Iniciei o git:

```bash
git init
```

Realizei o primeiro commit:

```bash
git commit -m "Parvi commit"
```

Adicionei o repositório:

```bash
git remote add origin https://github.com/WorkedTime/DesafioParvi.git
git branch -M main
git push -u origin main --force
```

Link do Repositorio do Git (https://github.com/WorkedTime/DesafioParvi.git)
