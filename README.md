# **Desafio - RPA Python - Grupo Parvi**

Etapas do Desafio
1. **Web Scraping com Selenium**
2. **Processamento de Dados com Pandas**
3. **Envio de Relatório por E-mail (Extra)**

## **Passo 1: Configurar o Ambiente de Desenvolvimento**

### **1.1 Instalei o python**

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
Dentro do diretório do projeto, abri um terminal e executei o seguinte comando:
```bash
python -m venv venv
```
Ativei o ambiente:
  ```bash
  venv\Scripts\activate
  ```

### **1.4 Instalei as Dependências**
Instalei as bibliotecas utiizando os seguintes comandos:
```bash
pip install selenium pandas python-dotenv
```
Gerei o arquivo `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### **1.5 Configurei o WebDriver**
Baixei o **ChromeDriver** compatível com a versão do meu Google Chrome:   
Extrai o arquivo e adicionei o `chromedriver.exe` na pasta `webdriver` do projeto.


## **Passo 2: Estruturei o Projeto**
Crie a seguinte estrutura de diretórios para deixar o projeto mais organizado:
```
📂 RPA_Quotes
 ┣ 📂 venv              # Ambiente virtual
 ┣ 📂 data              # Pasta para armazenar arquivos CSV
 ┣ 📂 webdriver         # Pasta para o ChromeDriver
 ┣ 📜 .env              # Credenciais para envio de e-mail
 ┣ 📜 main.py           # Arquivo principal do projeto
 ┣ 📜 requirements.txt  # Dependências
 ┣ 📜 README.md         # Instruções do projeto
```


## **Passo 3: Implementei Web Scraping com Selenium**
Crie o arquivo `main.py` e adicione:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://quotes.toscrape.com"
driver.get(url)

time.sleep(5)

quotes = driver.find_elements(By.CLASS_NAME, "quote")

with open("data/quotes.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Citação", "Autor", "Tags"])

    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]

        writer.writerow([text, author, ", ".join(tags)])

driver.quit()
print("Arquivo 'quotes.csv' gerado com sucesso!")
```
Executei o script para gerar o `quotes.csv`.



## **Passo 4: Processei os Dados com Pandas**
Adicionei ao `main.py`:
```python
import pandas as pd

df = pd.read_csv("data/quotes.csv")

print(f"Total de citações: {len(df)}")

autor_mais_frequente = df["Autor"].value_counts().idxmax()
print(f"Autor mais recorrente: {autor_mais_frequente}")

tag_mais_frequente = df["Tags"].str.split(", ").explode().value_counts().idxmax()
print(f"Tag mais utilizada: {tag_mais_frequente}")
```


## **Passo 5: Executei o envio de Relatório por E-mail**
Criei um arquivo `.env` com as minhas credenciais:
```plaintext
EMAIL_USER=desafio.parvi@gmail.com
EMAIL_PASS=iwsm useg xuwg zhlo
```
Adicionei ao `main.py`:
```python
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

def enviar_email():
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Citações'
    msg['From'] = user
    msg['To'] = 'paulo.andre@parvi.com.br', 'thiago.jose@parvi.com.br'
    msg.set_content(f"Total de citações: {len(df)}\n"
                    f"Autor mais recorrente: {autor_mais_frequente}\n"
                    f"Tag mais utilizada: {tag_mais_frequente}")
    
    with open("data/quotes.csv", "rb") as f:
        msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="quotes.csv")
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")

enviar_email()
```


## **Passo 6: Após eu finalizar todo o andamento do projeto, versionei ele no meu git**
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
git push -u origin main
```
Link do Repositorio do Git (https://github.com/WorkedTime/DesafioParvi.git)