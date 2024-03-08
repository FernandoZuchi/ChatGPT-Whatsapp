from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import openai
import PySimpleGUI as sg

# ----------------------------------------------------------------------------------------- API ----------------------------------------------------------------------------------------------------------#
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

api = requests.get("https://editacodigo.com.br/index/api-whatsapp/sm0WzC0H4aa1zgZyKGNb0jbV8LFrFBgN" ,  headers=agent)
time.sleep(1)
api = api.text
api = api.split(".n.")
token1 = api[0].strip()
token2 = api[1].strip()
token3 = api[2].strip()
bolinha_notificacao = api[3].strip()
contato_cliente = api[4].strip()
caixa_msg = api[5].strip()
msg_cliente = api[6].strip()    
# ----------------------------------------------------------------------------------------- BOT ----------------------------------------------------------------------------------------------------------#
mensagem_enviada = False  # Adiciona uma variável de controle

def bot():
    global mensagem_enviada  
    try:
        if not mensagem_enviada:
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
            sistema = 'Você é o Nexus, a inteligência artificial da Codi Academy, você é um professor excelente de programação FullStack. Seu objetivo é auxiliar no aprendizado dos alunos da Codi Academy, responder perguntas voltadas a programação, auiliar em projetos, fornecer informações e códigos'
            
            # Processa a mensagem na API da IA
            chave_api = apiopenai.strip()
            editacodigo = 'sm0WzC0H4aa1zgZyKGNb0jbV8LFrFBgN'
            resposta = requests.get("https://editacodigo.com.br/gpt/index.php",params={'pagina': editacodigo,'sistema': sistema, 'chave_api': chave_api, 'mensagem_usuario': msg}, headers=agent)
            time.sleep(1)
            resposta = resposta.text

            # Responde a mensagem 
            campo_de_texto = driver.find_element(By.XPATH,caixa_msg)
            campo_de_texto.click()
            time.sleep(1)
            # Limpar o campo de texto
            for i in range(len(campo_de_texto.text)):
                campo_de_texto.send_keys(Keys.BACKSPACE)

            # Enviar a resposta
            campo_de_texto.send_keys(resposta, Keys.ENTER)
            time.sleep(10)
            
            for char in resposta:
                campo_de_texto.send_keys(char)
                time.sleep(0.1)  # Pausa para simular a digitação
                
            # Pressiona ENTER quando a mensagem estiver completa
            campo_de_texto.send_keys(Keys.ENTER)
            time.sleep(5)  # Tempo de espera após o envio

            # Fecha o contato
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            mensagem_enviada = True
        
    except:
        print('buscando novas notificações')


# ----------------------------------------------------------------------------------------- TELA ----------------------------------------------------------------------------------------------------------#

tela1 = [
    [sg.Text('SENHA')],
    [sg.Input(key='senha', password_char='*')],
    [sg.Button('ENTRAR')],

]

tela2 = [
    [sg.Text('Interface do Chatbot com inteligência artificial')],
    [sg.Text('Insira a API da Openai')],
    [sg.Input(key='apiopenai')],
    [sg.Multiline(size=(80,20),key='texto')],
    [sg.Text('Tenha o celular em mãos')],
    [sg.Text('Clique abaixo para capturar o QRCode')],
    [sg.Button('Capturar QRCode')],
]

# ----------------------------------------------------------------------------------------- PUXAR TELAS ----------------------------------------------------------------------------------------------------------#



windows1 = sg.Window('IA BOT', layout= tela1)
windows2 = sg.Window('Tela 2', layout= tela2)

while True:
    event, values = windows1.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'ENTRAR': 
        senha = values['senha']
        if senha == token1:
            windows1.close()
            event2, value2 = windows2.read()
            if event2 == 'Capturar QRCode':
                apiopenai = value2['apiopenai']
                texto = value2['texto']
                windows2.close()
                 # Abrir o navegador adaptado para automação
                dir_path = os.getcwd()
                chrome_options2 = Options()
                chrome_options2.add_argument(r"user-data-dir=" + dir_path + "profile/zap")
                driver = webdriver.Chrome(options=chrome_options2)
                driver.get('https://web.whatsapp.com/')
                time.sleep(10)
                while True:
                    bot()