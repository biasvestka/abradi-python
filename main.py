import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


def processar_paginas_inicial_final(pagina_inicial, pagina_final):
    for i in range(pagina_inicial, pagina_final + 1):
        url = f"https://abradi.com.br/agentes-digitais/page/{i}/"
        print(f"Processando {url}")
        processar_pagina(url)


def processar_pagina(url):
    driver.get(url)

    agencias = extrair_agencias(url)

    for agencia_url in agencias:
        dados_contato = extrair_dados_contato(agencia_url)
        if dados_contato:
            salvar_dados_json('dados.json', dados_contato)


def extrair_agencias(url):
    agencias = []

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.some-agency-selector')))
        elementos_agencias = driver.find_elements(By.CSS_SELECTOR, '.some-agency-selector')

        for elemento in elementos_agencias:
            agencia_url = elemento.get_attribute('href')
            agencias.append(agencia_url)

    except Exception as e:
        print(f"Erro ao extrair as agências da URL {url}: {e}")

    return agencias


def extrair_dados_contato(url):
    driver.get(url)
    dados = {}

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.section-single-agentes-digitais')))

        try:
            email = driver.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]').text
            dados['email'] = email
        except:
            dados['email'] = "Não informado"

        try:
            telefone = driver.find_element(By.CSS_SELECTOR, 'a[href^="https://api.whatsapp.com/send?phone="]').text
            dados['telefone'] = telefone
        except:
            dados['telefone'] = "Não informado"

        try:
            nome_contato = driver.find_element(By.CSS_SELECTOR, '.aperto-de-maos-azul').text
            dados['nome_contato'] = nome_contato
        except:
            dados['nome_contato'] = "Não informado"

        try:
            site = driver.find_element(By.CSS_SELECTOR, 'a[href^="http"]').text
            dados['site'] = site
        except:
            dados['site'] = "Não informado"

        return dados

    except Exception as e:
        print(f"Erro ao extrair dados da URL {url}: {e}")
        return None


def salvar_dados_json(caminho_arquivo, dados_novos):
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w') as file:
            json.dump([], file)

    with open(caminho_arquivo, 'r') as file:
        try:
            dados_existentes = json.load(file)
        except json.JSONDecodeError:
            dados_existentes = []

    dados_existentes.append(dados_novos)

    with open(caminho_arquivo, 'w') as file:
        json.dump(dados_existentes, file, indent=4)


processar_paginas_inicial_final(3, 5)

driver.quit()
