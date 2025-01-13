from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

''' ESSA É PRIMEIRA VERSÃO DO WEB SCRAPING UTILIZADO PARA BUSCAR AS PROMOÇÕES DOS JOGOS, FOI FEITA EM SELENIUM!
    COM ALGUNS ESTUDOS, OBSERVEI QUE O SELENIUM NÃO SERIA UMA BOA OPÇÃO PARA ESTE PROJETO, POIS É UMA FERRAMENTA QUE TEM
    COMO OBJETIVO A AUTOMAÇÃO WEB UTILIZANDO PYTHON, E, POR MAIS QUE EU CONSIGA ATINGIR MEUS OBJETIVOS COM ESSA FERRAMENTA,
    A FERRAMENTA BEAUTIFUL SOAP SE ENCAIXA MAIS POR SER MAIS AGIL PARA WEB SCRAPING! '''


# O SERVIÇO WEB NO QUAL EU APLIQUEI A AUTOMAÇÃO, NO CASO, O CHROME
browser_service = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=browser_service)


# CLASSE COM AS FUNÇÕES DE WEB SCRAPING CONTRUIDAS EM SELEMIUM
class DealBot:

    ''' ESSA FUNÇÃO IRÁ BUSCAR TODOS NA SESSÃO DE JOGOS POPULARES NO SITE GG.DEALS UTILIZANDO SUA URL '''
    def see_popular_games(self):
        browser.get('https://gg.deals/games/')
        sleep(0.5)
        game_list = {}
        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').text
            try:
                price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            except:
                price = game_item.find_element(By.CLASS_NAME, 'unavailable-label').text
            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                game_list[name] = {price: discount}
            except:
                game_list[name] = {price: 'NOT DISCOUNT'}
        
        return game_list

    ''' ESSA FUNÇÃO IRÁ BUSCAR TODOS OS JOGOS GRATUITOS NA SESSÃO DE JOGOS GRATUITOS NO SITE GG.DEALS UTILIZANDO SUA URL

        ESSA FUNÇÃO NÃO FOI RETORNADA NO TESTE DO DISCORD, POR ISSO NÃO POSSUI UM RETORNO, APENAS PRINTS
    '''
    def see_free_games(self):
        browser.get('https://gg.deals/games/?maxPrice=0&sort=wanted')
        sleep(0.5)
        game_list = {}
        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        game_indice = 1 # É USADO NA CONTAGEM DE JOGOS EXIBIDOS
        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').get_attribute('data-title-multiline-auto-hide')
            price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                print(f'GAME {game_indice} --- {name}: {price} - DISCOUNT: {discount}')
            except:
                print(f'GAME {game_indice} --- {name}')
            game_indice += 1
        sleep(20)

    ''' ESSA FUNÇÃO IRÁ BUSCAR AS MELHORES PROMOÇÕES NA SESSÃO DE BEST DEALS NO SITE GG.DEALS UTILIZANDO SUA URL

        ESSA FUNÇÃO NÃO FOI RETORNADA NO TESTE DO DISCORD, POR ISSO NÃO POSSUI UM RETORNO, APENAS PRINTS
    '''
    def see_best_deals(self):
        browser.get('https://gg.deals/deals/')
        sleep(0.5)

        game_list = {}
        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        game_indice = 1

        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').get_attribute('data-title-auto-hide')
            try:
                price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            except:
                price = game_item.find_element(By.CLASS_NAME, 'unavailable-label').text

            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                game_list[name] = {price: discount}
            except:
                game_list[name] = {price: 'NOT DISCOUNT'}
            game_indice += 1
        
        return game_list

    ''' ESSA FUNÇÃO IRÁ BUSCAR AS NOVAS PROMOÇÕES NA SESSÃO DE NEW DEALS NO SITE GG.DEALS UTILIZANDO SUA URL

        ESSA FUNÇÃO NÃO FOI RETORNADA NO TESTE DO DISCORD, POR ISSO NÃO POSSUI UM RETORNO, APENAS PRINTS
    '''
    def see_new_deals(self):
        browser.get('https://gg.deals/deals/new-deals/')
        sleep(0.5)

        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        game_indice = 1

        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').get_attribute('data-title-auto-hide')
            price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                print(f'GAME {game_indice} --- {name}: {price} - DISCOUNT: {discount}')
            except:
                print(f'GAME {game_indice} --- {name}: {price} - NOT DISCOUNT')
            game_indice += 1
        sleep(20)

    ''' ESSA FUNÇÃO IRÁ BUSCAR OS JOGOS QUE ESTÃO COM SEUS MENORES PREÇOES DESDE SEUS LANÇAMENTOS NO SITE GG.DEALS UTILIZANDO SUA URL

        ESSA FUNÇÃO NÃO FOI RETORNADA NO TESTE DO DISCORD, POR ISSO NÃO POSSUI UM RETORNO, APENAS PRINTS
    '''
    def see_game_historical_low(self):
        browser.get('https://gg.deals/deals/historical-lows/')
        sleep(0.5)

        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        game_indice = 1

        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').get_attribute('data-title-auto-hide')
            price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                print(f'GAME {game_indice} --- {name}: {price} - DISCOUNT: {discount}')
            except:
                print(f'GAME {game_indice} --- {name}: {price} - NOT DISCOUNT')
            game_indice += 1
        sleep(20)