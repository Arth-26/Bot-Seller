from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep

browser_service = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=browser_service)

class AutomatiBot:

    def see_promotions(self):
        browser.get('https://gg.deals')
        sleep(1)
        browser.find_element('xpath', '/html/body/div[2]/div/section[1]/div/div[1]/a').click()
        game_list = {}
        game_list_container = browser.find_elements('class', 'game-item')
        for game_item in game_list_container:
            add_item = {game_item : {}}
            game_list.append
        sleep(20)