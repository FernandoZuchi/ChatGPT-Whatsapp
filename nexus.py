from selenium import webdriver
import time
import os
import requests
import openai
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "profile/zap")
driver = webdriver.Chrome(options=chrome_options2)
driver.get('https://web.whatsapp.com/')
time.sleep(120)

# API do Edita Código 
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

api = requests.get("https://editacodigo.com.br/index/api-whatsapp/sm0WzC0H4aa1zgZyKGNb0jbV8LFrFBgN" ,  headers=agent)
time.sleep(1)
api = api.text
api = api.split(".n.")
bolinha_notificacao = api[3].strip()
contato_cliente = api[4].strip()
caixa_msg = api[5].strip()
msg_cliente = api[6].strip()	

def bot():  
    try:
        # Pegar a notificação e abrir ela
        bolinha = driver.find_element(By.CLASS_NAME,bolinha_notificacao)
        bolinha = driver.find_elements(By.CLASS_NAME,bolinha_notificacao)
        clica_bolinha = bolinha[-1]
        acao_bolinha = webdriver.common.action_chains.ActionChains(driver)
        acao_bolinha.move_to_element_with_offset(clica_bolinha,0,-20)
        acao_bolinha.click()
        acao_bolinha.perform()
        acao_bolinha.click()
        acao_bolinha.perform()
        print('Buscando novas notificações...')
        
        # Pegar a mensagem que chegou
        todas_as_msg = driver.find_elements(By.CLASS_NAME, msg_cliente)
        todas_as_msg_texto = [e.text for e in todas_as_msg]
        msg = todas_as_msg_texto[-1]
        print()
        
        # Customizando a IA
        sistema = 'DE FORMA ALGUMA É PERMITIDO QUEBRAR A LINHA, MESMO QUANDO NECESSÁRIO Você é o Nexus, a inteligência artificial da Codi Academy, você é um professor excelente de programação FullStack.Envie a mensagem sem quebra de linhas. Seu objetivo é auxiliar no aprendizado dos alunos da Codi Academy LEMBRANDO, ENVIE APENAS UMA MENSAGEM, EVITE A TODO CUSTO A QUEBRA DE LINHA, FAÇA SUA RESPOSTA SEM QUEBRAR LINHAS, responder perguntas voltadas a programação, auiliar em projetos, fornecer informações e códigos. DE FORMA ALGUMA É PERMITIDO QUEBRAR A LINHA, MESMO QUANDO NECESSÁRIO'
        
        # Processa a mensagem na API da IA
        chave_api = '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'
        editacodigo = 'sm0WzC0H4aa1zgZyKGNb0jbV8LFrFBgN'
        resposta = requests.get("https://editacodigo.com.br/gpt/index.php",params={'pagina': editacodigo,'sistema': sistema, 'chave_api': chave_api, 'mensagem_usuario': msg}, headers=agent)
        time.sleep(1)
        resposta = resposta.text

        # Responde a mensagem 
        campo_de_texto = driver.find_element(By.XPATH,caixa_msg)
        campo_de_texto.click()
        time.sleep(10)
        campo_de_texto.send_keys(resposta)

        while True:
            time.sleep(1)
            if campo_de_texto == resposta:
                campo_de_texto.send_keys(Keys.ENTER)
                break
        
        # Fecha o contato
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
    except:
        print('buscando novas notificações')

while True:
    bot()