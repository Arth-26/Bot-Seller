import requests
from bs4 import BeautifulSoup
from time import sleep

class ScrapignBot():

    def see_popular_games(self):
        
        url = 'https://gg.deals/games/'

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
        
        request = requests.get(url, headers=headers)
        parsed_html = BeautifulSoup(request.text, 'html.parser')

        game_list_div = parsed_html.find('div', class_='list-items')
        game_list_elements = game_list_div.find_all('div', class_='game-item')

        for game_item in game_list_elements:
            print(game_item)
            break



        