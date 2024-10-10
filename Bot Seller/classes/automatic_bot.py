from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

browser_service = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=browser_service)

class AutomatiBot:

    def see_promotions(self):
        browser.get('https://gg.deals')
        sleep(0.5)
        browser.find_element(By.XPATH, '/html/body/div[2]/div/section[1]/div/div[1]/a').click()
        game_list = {}
        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        game_indice = 1
        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').get_attribute('data-title-multiline-auto-hide')
            price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                print(f'GAME {game_indice} --- {name}: {price} - DISCOUNT: {discount}')
            except:
                print(f'GAME {game_indice} --- {name}: {price} - NOT DISCOUNT')
            game_indice += 1
        sleep(20)

    def see_free_games(self):
        browser.get('https://gg.deals')
        sleep(0.5)
        browser.find_element(By.XPATH, '/html/body/div[2]/div/section[1]/div/div[1]/a').click()
        sleep(0.5)
        price_filter = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[1]/div/form/div/div/div[1]/div[3]')
        min_price = price_filter.find_element(By.ID, 'MainGamesSearch_minPrice-input-filter')
        max_price = price_filter.find_element(By.ID, 'MainGamesSearch_maxPrice-input-filter')

        min_price.send_keys('0')
        max_price.send_keys('0' + Keys.ENTER)
        sleep(0.5)

        game_list_div = browser.find_element(By.CLASS_NAME, 'list-items')
        game_list_elements = game_list_div.find_elements(By.CLASS_NAME, 'game-item')
        game_indice = 1
        for game_item in game_list_elements:
            name = game_item.find_element(By.CLASS_NAME, 'game-info-title').get_attribute('data-title-multiline-auto-hide')
            price = game_item.find_element(By.CLASS_NAME, 'price-inner').text
            try:
                discount = game_item.find_element(By.CLASS_NAME, 'discount').text
                print(f'GAME {game_indice} --- {name}: {price} - DISCOUNT: {discount}')
            except:
                print(f'GAME {game_indice} --- {name}: {price} - NOT DISCOUNT')
            game_indice += 1
        sleep(20)
