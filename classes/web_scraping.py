from .utils import see_game_list, update_daily_deals

class ScrapingBot():

    '''AQUI EU CHAMO AS FUNÇÕES DO UTILS PASSANDO AS URL COMO PARÂMENTRO. 
    ESSAS FUNÇÕES SÃO USADAS COMO RETORNO DOS DADOS NAS FUNÇÕES CONSTRUIDAS PARA O DISCORD'''

    def see_popular_games(self):

        url = 'https://gg.deals/games/'

        return see_game_list(url)
    
    def see_best_deals(self):

        url = 'https://gg.deals/deals/'

        return see_game_list(url)
    
    def see_free_games(self):

        url = 'https://gg.deals/games/?maxPrice=0&sort=wanted'

        return see_game_list(url)
    
    def see_new_deals(self):

        url = 'https://gg.deals/deals/new-deals/'

        return see_game_list(url)
    
    def see_game_historical_low(self):

        url = 'https://gg.deals/deals/historical-lows/'

        return see_game_list(url)
    
    def daily_games_update(self):

        list_games = update_daily_deals()

        return list_games



        