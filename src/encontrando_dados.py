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

#1.Instalação do driver do Chrome, além de baixar a versão mais recente para a sua máquina, iniciando o navegador e se conectando ao Selenium.
#2.Acesso ao site com o driver.get e armazenando na lista quote_lists, executando o script em loop enquanto verdadeiro para encontro das citações por busca de elementos via name, também manusendo com uso de except para qualquer erro de busca.
#3.Click de botão next para permanência de buscas em outras páginas do mesmo site.
#4.Tratativa de erro caso a busca falhe, além de aviso e encerramento visível da função.
#5.Encerramento do Driver.
#6.Cria o arquivo (csv)

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
