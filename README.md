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
 ┣ 📂 data              	# Pasta armazenando o arquivo CSV que foi gerado
    ┣ 📜 citacoes.csv      		# Armazenamento gerado dos arquivos de busca no CSV (Dentro da pasta data)
 ┣ 📂 src               	# Funções guardadas que serão chamadas pela main   
    ┣ 📂 _pycache_         	# Arquivos compilados de módulos - Oculto
    ┣ 📜 criando_csv.py			# Função criada exclusivamente para crição do CSV
    ┣ 📜 encontrando_dados.py  		# Função criada para busca de dados via Web(WebScraping)
    ┣ 📜 processar_dados.py		# Função criada para leitura e novo filtro de dados do CSV
    ┣ 📜 enviar_email.py		# Função criada para envio dos dados pós filtros e finalização de contagens para os e-mails cadastrados na lista do arquivo .env
 ┣ 📂 venv              	# Ambiente virtual - Oculto
 ┣ 📜 .env              	# Credenciais para envio de e-mail - Oculto
 ┣ 📜 .env.examples     	# Credenciais não reais para exemplo de e-mail para o git  
 ┣ 📜 .gitignore        	# Biblioteca git para não uso de dados sensíveis dos usuários e desenvolvedor
 ┣ 📜 main.py           	# Arquivo principal do projeto
 ┣ 📜 README.md         	# Instruções do projeto
 ┣ 📜 requirements.txt  	# Dependências

```

## **Passo 3: Implementei Web Scraping com Selenium**

Criei uma função chamada encontrando_dados(): para envio dos arquivos buscados via automação e criação do arquivo CSV pós filtro para futuro uso na  `main.py` e adicionei todos os imports e suas referências para busca dos dados:


import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

Part I - Busca de dadps via URL e filtro de buscas

load_dotenv(override=True)

def encontrando_dados():
   service = Service(ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service)
   busca = os.getenv("URL")
   driver.get(busca)
   quotes_list = []
   while True:
       try:
           WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))
           #Coleta as citações na página atual
           quotes = driver.find_elements(By.CLASS_NAME, "quote")
           for quote in quotes:
               texts = [texto.text for texto in quote.find_elements(By.CLASS_NAME, "text")]
               author = quote.find_element(By.CLASS_NAME, "author").text
               tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
               quotes_list.append((texts, author, tags))
               print(f"{texts} - {author} - {tags}")
           #Tenta encontrar o botão "Next"
           next_button = driver.find_element(By.CSS_SELECTOR, 'li.next > a')
           next_button.click()
       except (NoSuchElementException, TimeoutException):
           print("\nNavegação finalizada por erro de tempo ou os elementos solicitados não foram encontrados!")
           break
       except Exception as e:
           print(f"\nOcorreu um erro inesperado: {e}")
           break
   driver.quit()
   print(f"\nTotal de citações coletadas: {len(quotes_list)}")
   return{
       "total":quotes_list
       }

## **Passo 4: Realizei a criação dos dados como tabela com o Pandas**

Criei uma função chamada criando_csv(): para receber os arquivos buscados via automação e criação do arquivo CSV para uso na  `main.py` e adicionei todos os imports e suas referências para criação dos dados na tabela:


import csv
import os

from src.encontrando_dados import encontrando_dados

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

    #total_lista = encontrando_dados()
    #total = total_lista["total"]

    try:
        with open(arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(["Texto", "Autor", "Tags"])
            writer.writerows(total)
            print(f"\nArquivo csv criado com sucesso dentro da pasta {pasta}!")

    except Exception as e:
        print(f"\nErro ao criar o arquivo CSV: {e}")
    return {
        "status": "CSV criado com sucesso",
        "caminho": arquivo
    }

## **Passo 5: Processei os dados para contagem de mais repetidos e os que haviam mais contagens repetidas com o Pandas:**

Criei uma função processando_dados(): para filtro final dos arquivos buscados para posterior envio via e-mail alocada na  `main.py`  adicionei todos os imports para determinar especificamente os dados que desejo:


import ast


import pandas as pd

def processando_dados() -> dict:
    try:
        df = pd.read_csv("data/citacoes.csv")

    total_quotes = df["Texto"].value_counts().count()
        print(f"\nQuantidade total de citações: {total_quotes}")

    autor_mais_frequente = df["Autor"].value_counts().idxmax()
        print(f"Autor mais recorrente: {autor_mais_frequente}")

    tag_mais_frequente = (df["Tags"].apply(ast.literal_eval).explode().str.capitalize().value_counts().idxmax())
        print(f"Tag mais utilizada: {tag_mais_frequente}\n")

    return {
            'Citacoes': int(total_quotes),
            'Autor': autor_mais_frequente,
            'Tag': tag_mais_frequente
        }

    except FileNotFoundError:
        print("Erro! Arquivo CSV não encontrado.")
        #raise
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        #raise

## Passo 6: Envio de dados via e-mail pelo smtplib

Criei uma função chamada enviar_email(): para envio dos arquivos buscados via e-mail também chamada na  `main.py`  adicionei todos os imports e suas referências para enviar apenas dados específicos no corpo(body) do e-mail:


import os

import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

from src.processando_dados import processando_dados

#Parte III - Enviando o relatório via e-mail
load_dotenv(override=True)

def enviar_email():

    #total = processando_dados()
    citacoes = (total["Citacoes"])
    autor = (total["Autor"])
    tags = (total["Tag"])

    user = os.getenv("EMAIL")
    password = os.getenv("PASS")
    email_list = os.getenv("EMAIL_LIST")

    if email_list:
        emails = email_list.split(",")

    for email in emails:
            print(f"Sucesso! Enviado para: {email}")
    else:
        print("A variável EMAIL_LIST não foi definida no arquivo .env.")

    if not user or not password:
        print("Erro: EMAIL ou PASS não estão definidos no .env")
        return

    #Envio de e-mail sendo remetente, destinatário e corpo da mensagem definidos
    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = user
    msg['To'] = email_list
    msg.set_content(f"Arquivos gerados do CSV:\n Total de {citacoes} Citações\n O autor mais recorrente é: {autor}\n A tag mais utilizada é: {tags}")

    try:
        with open("data/citacoes.csv", "rb") as f:
            msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="citacoes.csv")
    except FileNotFoundError:
        print("Erro! Arquivo csv não encontrado.")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
            print("\nE-mail enviado com sucesso! CONCLUIDO!!!")
    except Exception as e:
        print(f"Falha ao enviar e-mail! \n {e}")
    return {
        "status": "E-mail enviado com sucesso",
        "destinatarios": email_list
    }

## **Passo 7: Após finalizar todo o andamento do projeto, versionei ele no meu git**

Realizei a instalação e configuração do git na minha máquina:


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
git branch -m main
git push -u origin main --force
```

Link do Repositorio do Git (https://github.com/WorkedTime/DesafioParvi.git)
