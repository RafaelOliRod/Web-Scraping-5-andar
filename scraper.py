import os
import re
import io
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup  # Importando BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.firefox.options import Options
from flask import send_file

# Inicializar a variável global driver fora da função scrape()
driver = None

# Função para inicializar o driver


def iniciar_driver():
    global driver
    try:
        service = FirefoxService(
            executable_path=GeckoDriverManager().install())
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--start-minimized")
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(60)
        driver.maximize_window()
        driver.implicitly_wait(10)
    except Exception as e:
        print("Ocorreu um erro ao inicializar o driver:", e)

# Função para clicar no botão "Ver mais"


def click_ver_mais(driver):
    try:
        ver_mais_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(text(),'Ver mais')]")
            )
        )
        ver_mais_button.click()
        return True
    except TimeoutException:
        print("Tempo limite excedido. Não foi possível encontrar o botão 'Ver mais'.")
        return False


def scrape(url):
    global driver
    # Verificar se o driver foi inicializado com sucesso
    if not driver:
        print("O driver não foi inicializado. Inicializando...")
        iniciar_driver()

    try:
        driver.get(url)

        # Aguardar um tempo para o carregamento inicial da página
        time.sleep(5)

        # Loop para clicar no botão "Ver mais" até que não haja mais elementos para carregar
        while True:
            if not click_ver_mais(driver):
                break
            # Aguardar um tempo para o carregamento após cada clique
            time.sleep(5)

        # Após carregar todas as informações, prosseguir com o scraping
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        data = []

        # Função para extrair os dados de uma postagem
        def extract_data(post):
            # Extrair informações específicas, exemplo título e preço
            aria_label = post.get("aria-label")
            title = aria_label.split(".")[0] if aria_label else 'No Title'

            # Extrair link do imóvel
            link_element = post.find('a', class_='sc-1d0oyoa-0 bfDoiv')
            link = link_element['href'] if link_element else 'No Link'

            # Extrair informações adicionais
            size = post.select_one(
                "h3.CozyTypography.xih2fc.EKXjIf.A68t3o").text.strip()

            # Extrair preço do aluguel
            price_rent_element = post.select_one(
                "h3.CozyTypography.xih2fc._72Hu5c.Ci-jp3")
            price_rent = price_rent_element.text.strip(
            ) if price_rent_element else 'No Rent Price'

            # Extrair preço total
            price_total_element = post.select_one(
                "h3.CozyTypography.xih2fc.EKXjIf.EqjlRj")
            price_total = price_total_element.text.strip(
            ) if price_total_element else 'No Total Price'

            address = post.select_one(
                "h2.CozyTypography.sc-bZnhIo.gBFgNb.xih2fc._72Hu5c.Ci-jp3").text.strip()

            # Extrair o bairro e a cidade
            if ',' in address and '·' in address:
                neighborhood = address.split(',')[1].split('·')[0].strip()
                city = address.split('·')[-1].strip()
            else:
                neighborhood = 'No Neighborhood'
                city = 'No City'

            # Extrair número de quartos e vagas de garagem
            size_parts = size.split('·')
            num_quartos = size_parts[1].strip().split()[
                0] if len(size_parts) > 1 else 0
            num_vagas = size_parts[2].strip().split()[
                0] if len(size_parts) > 2 else 0

            data.append([size, num_quartos, num_vagas, address,
                        neighborhood, city, price_rent, price_total, link])

        posts = soup.find_all('div', class_='sc-1uhd8i-1 bTndEd')

        for post in posts:
            extract_data(post)

        df = pd.DataFrame(data, columns=['Tamanho m²', 'Quartos', 'Vagas de Garagem',
                                         'Endereço', 'Bairro', 'Cidade', 'Preço Aluguel', 'Preço Total', 'Link'])

        df = df.drop_duplicates()

        # Processar a coluna 'Tamanho m²' para remover tudo após o primeiro numeral
        df['Tamanho m²'] = df['Tamanho m²'].apply(lambda x: re.match(
            r'\d+', x).group() if re.match(r'\d+', x) else x)

        # Remover texto após a vírgula na coluna de endereço
        df['Endereço'] = df['Endereço'].apply(
            lambda x: x.split(',')[0] if ',' in x else x)

        # Converter tipos de dados para string
        df = df.astype(str)

        # Remover caracteres não numéricos dos preços
        df['Preço Aluguel'] = df['Preço Aluguel'].str.replace(
            r'\D', '', regex=True)
        df['Preço Total'] = df['Preço Total'].str.replace(
            r'\D', '', regex=True)

        # Reordenar as colunas para ter "Preço Total" após "Preço Aluguel"
        df = df[['Endereço', 'Bairro', 'Cidade', 'Tamanho m²',
                 'Quartos', 'Vagas de Garagem', 'Preço Aluguel', 'Preço Total', 'Link']]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        output.seek(0)
        return output.getvalue()

    except Exception as e:
        print("Ocorreu um erro durante a execução:", e)
    finally:
        if driver:
            driver.quit()
