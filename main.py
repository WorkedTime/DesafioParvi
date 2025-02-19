#Bibliotecas Importadas
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

#Parte 1 - Web Scraping com Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://quotes.toscrape.com/js-delayed/"
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


#Parte 2 - Processamento de Dados com Pandas
df = pd.read_csv("data/quotes.csv")

print(f"Total de citações: {len(df)}")

autor_mais_frequente = df["Autor"].value_counts().idxmax()
print(f"Autor mais recorrente: {autor_mais_frequente}")

tag_mais_frequente = df["Tags"].str.split(", ").explode().value_counts().idxmax()
print(f"Tag mais utilizada: {tag_mais_frequente}")


#Parte 3 - Envio de Relatório por E-mail (Extra)
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
