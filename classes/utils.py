import requests
from bs4 import BeautifulSoup
from time import sleep

def see_game_list(url):
        
        path = url

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
        
        request = requests.get(path, headers=headers)
        parsed_html = BeautifulSoup(request.text, 'html.parser')

        storage_list = {}


        game_list_div = parsed_html.find('div', class_='list-items')
        game_list_elements = game_list_div.find_all('div', class_='game-item')

        for game_item in game_list_elements:
            try:
                name = game_item.find('a', class_='title-inner').get_text()
            except:
                name = game_item.find('a', class_='game-info-title').get_text()
            try:
                price = game_item.find('span', class_='price-inner').get_text()
            except:
                price = game_item.find('span', class_='unavailable-label').get_text()
            try:
                discount = game_item.find('span', 'discount').get_text()
                storage_list[name] = {price: discount}
            except:
                storage_list[name] = {price: 'NOT DISCOUNT'}
            
        return storage_list