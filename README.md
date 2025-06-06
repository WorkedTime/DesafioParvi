
# 🚀 Desafio RPA Python – Grupo Parvi

Automação completa com Python que realiza web scraping de citações, processa os dados e envia um relatório por e-mail.

## 📌 Funcionalidades:

- 🔍 Web scraping com Selenium
- 📊 Processamento de dados com Pandas
- 📧 Envio de relatório CSV por e-mail
- 🗂️ Organização modular do código

## 🛠 Tecnologias Usadas:

- Python 3.13.3
- Selenium
- Pandas
- WebDriver Manager
- Python-dotenv
- smtplib

## ⚙️ Como Rodar:

```bash
git clone https://github.com/WorkedTime/DesafioParvi.git
cd DesafioParvi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📦Preencha o arquivo `.env` com os dados:

EMAIL=seuemail@gmail.com
PASS=suasenha               
EMAIL_LIST=destinatario1@gmail.com,destinatario2@gmail.com
URL=http://quotes.toscrape.com/

## 🧠Execute o projeto:

python main.py

## 📁 Estrutura de Pastas:

📦 DESAFIOPARVI_1.1
 ┣ 📂 data/   
 ┣ 📂 src/   
 ┣ 📜 main.py    
 ┣ 📜 .env      
 ┣ 📜 .env.example        
 ┣ 📜 requirements.txt       
 ┣ 📜 README.md       

## 📤 Envio por E-mail:

O script compõe uma mensagem com:

* Total de citações encontradas
* Autor mais frequente
* Tag mais comum

Em seguida, envia um e-mail com o CSV em anexo.

## 🔗 Repositório

🔗 GitHub - WorkedTime/DesafioParvi
