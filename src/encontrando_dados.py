import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

#Part I - Busca de dados via URL e filtro de buscas
def encontrando_dados(element: str = "quote" , busca_1: str = "text", busca_2: str = "author", busca_3: str = "tag") -> dict:
    """
    Realiza web scraping no site definido pela variável de ambiente 'URL',
    coletando citações, autores e tags.
    element (str): Busca principal relacionado a presença dos elementos mostrados na busca Web
    busca_1 (str): 1ª busca por dados escolhidos pelo usuário
    busca_2 (str): 2ª busca por dados escolhidos pelo usuário
    busca_3 (str): 3ª busca por dados escolhidos pelo usuário

    Returns:
        dict: Um dicionário com a chave "quotes" contendo uma lista de tuplas (texto, autor, tags).
    """

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    busca = os.getenv("URL")
    if not busca:
        print("Erro: variável de ambiente 'URL' não está definida.")
        driver.quit()
        return{}
    
    driver.get(busca)
    quotes_list = []

    while True:
        try:

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, element)))

            #Coleta as citações na página atual
            quotes = driver.find_elements(By.CLASS_NAME, element)
            for quote in quotes:
                texts = [texto.text for texto in quote.find_elements(By.CLASS_NAME, busca_1)]
                author = quote.find_element(By.CLASS_NAME, busca_2).text
                tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, busca_3)]
                quotes_list.append((texts, author, tags))
                print(f"{texts} - {author} - {tags}")

            #Tenta encontrar o botão "Next"
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.next > a'))
                )
                next_button.click()
            except TimeoutException:
                print("\nFim da navegação ou botão 'Next' não encontrado.")
                break

        except (NoSuchElementException, TimeoutException):
            print("\nNavegação finalizada por erro de tempo ou os elementos solicitados não foram encontrados!")
            break
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
            break

    driver.quit()
    print(f"\nTotal de citações coletadas: {len(quotes_list)}") 
    
    lista_dados = {"quotes": quotes_list}

    return lista_dados
