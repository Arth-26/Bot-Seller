from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

browser_service = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=browser_service)

class AutomatiBot:

    def see_promotions(self):
        browser.get('https://gg.deals')
        sleep(1)
        browser.find_element(By.XPATH, '/html/body/div[2]/div/section[1]/div/div[1]/a').click()
        game_list = {}
        game_list_elements = browser.find_element(By.CLASS_NAME, 'list-items')
        game_indice = 1
        for game_item in game_list_elements:
            print(game_item)
        #     game_name = game_item.find_element(By.CSS_SELECTOR, 'a[class="title"]).text')
        #     game_price = game_item.find_element(By.CSS_SELECTOR, 'a[class="price"]).text')
        #     game_list[game_indice] = {game_name: game_price}
        #     game_list.append
        #     game_indice += 1

        # for index, game in game_list:
        #     print(f'{index}: {game.items()}')
        sleep(20)