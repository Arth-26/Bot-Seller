import requests
from bs4 import BeautifulSoup
from time import sleep


''' NESSE ARQUIVO UTILS, EU ESCREVO AS FUNÇÕES QUE SERÃO USADAS PARA O WEB SCRAPING DAS INFORMAÇÕES QUE SERÃO UTILIZADAS NO MEU BOT!
    COMO ALGUMAS FUNÇÕES SEGUEM A MESMA LÓGICA, MUDANDO APENAS AS INFORMAÇÕES QUE SERÃO CONSULTADAS, EU ESCREVO APENAS UMA FUNÇÃO QUE
    POSSA SER REUTILIZADA VÁRIAS VEZES, ASSIM EVITANDO REPETIÇÃO DE CÓDIGO, E FACILITANDO POSSÍVEIS ATUALIZAÇÕES E MANUTENÇÕES'''


''' 
    ESSA É A FUNÇÃO QUE FARÁ A CONSULTA DOS JOGOS, ESSA FUNÇÃO RECEBE COMO PARAMETRO UMA URL QUE SERÁ PASSADA NA CHAMADA DESTA 
    FUNÇÃO NO ARQUIVO "web_scraping.py". 
'''    
def see_game_list(url):
        
        path = url

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
        
        request = requests.get(path, headers=headers)
        parsed_html = BeautifulSoup(request.text, 'html.parser')

        storage_list = {} # Dicionario que armazena os dados dos jogoS

        # Buscando elementos html de acordo com suas classes
        game_list_div = parsed_html.find('div', class_='list-items')
        game_list_elements = game_list_div.find_all('div', class_='game-item')

        # Para cada elemento referente a um jogo encontrado na consulta, irá buscar os seguintes dados:
        # NOME, PREÇO, DESCONTO
        for game_item in game_list_elements:
            # EM ALGUMAS SITUAÇÕES, OS ELEMENTOS VEM COM INFORMAÇÕES DIFERENTES, ENTÃO, 
            # É FEITO O TRATAMENTO PARA EVITAR ERROS
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
        

        # FORMATO DE RETORNO: lista = {nome: {preço: desconto}}
        return storage_list


''' 
    ESSA FUNÇÃO IRÁ CONSULTAR DIARIAMENTE O SITE GG.DEALS UTILIZANDO AS SCHEDULES TASKS DA BIBLIOTECA DO DISCORD E MOSTRARÁ
    AS PROMOÇÕES EM DESTAQUE EM UM INTERVALO DE TEMPO DEFINIDO NA CONSTRUÇÃO DA FUNÇÃO DO DISCORD
'''
def update_daily_deals(): 
     
    path = 'https://gg.deals'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
    
    request = requests.get(path, headers=headers)
    parsed_html = BeautifulSoup(request.text, 'html.parser')

    storage_list = {}

    # Dicionario contendo chaves que representa as sessões que serão usadas como paramentro na consulta
    # Os valores de cada chave é uma mensagem que será encaminhada para o título do EMBED contruidos nas funções do discord
    sessions = {'New deals': 'Novas Ofertas', 'Best deals': 'Melhores Ofertas', 'Historical lows': 'Baixa Histórica', 'Ending Soon': 'PROMOÇÕES ACABANDO!!'}

    for session, message in sessions.items():
        storage_list[f'{message}'] = {}
        game_list_div = parsed_html.find(attrs={"data-preset-name": f"{session}"})
        game_list = game_list_div.find('div', class_='list')
        game_list_elements = game_list.find_all('div', class_='game-item')

        for game_item in game_list_elements:
            try:
                name = game_item.find('a', class_='title').get_text(strip=True)
            except Exception as e:
                print(e)
            try:
                price = game_item.find('span', class_='price-inner').get_text(strip=True)
            except:
                price = game_item.find('span', class_='unavailable-label').get_text(strip=True)
            try:
                discount = game_item.find('span', 'discount').get_text(strip=True)
                # Como a mensagem tem que ser exibida no titulo do EMBED do discord, estarei retornando dentro do dicionario
                storage_list[f'{message}'][name] = {price: discount}
            except:
                storage_list[f'{message}'][name] = {price: 'NOT DISCOUNT'}
                

    # FORMATO DE RETORNO: lista = {sessão: {nome: {preço: desconto}}}
    return storage_list