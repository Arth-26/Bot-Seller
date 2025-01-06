import requests
from bs4 import BeautifulSoup
from time import sleep


''' NESSE ARQUIVO UTILS, EU ESCREVO AS FUNÇÕES QUE SERÃO USADAS PARA O WEB SCRAPING DAS INFORMAÇÕES QUE SERÃO UTILIZADAS NO MEU BOT!
    COMO ALGUMAS FUNÇÕES SEGUEM A MESMA LÓGICA, MUDANDO APENAS AS INFORMAÇÕES QUE SERÃO CONSULTADAS, EU ESCREVO APENAS UMA FUNÇÃO QUE
    POSSA SER REUTILIZADA VÁRIAS VEZES, ASSIM EVITANDO REPETIÇÃO DE CÓDIGO, E FACILITANDO POSSÍVEIS ATUALIZAÇÕES E MANUTENÇÕES'''


''' ESSA É A FUNÇÃO QUE FARÁ A CONSULTA DOS JOGOS, ESSA FUNÇÃO RECEBE COMO PARAMETRO UMA URL QUE SERÁ PASSADA NA CHAMADA DESTA 
    FUNÇÃO NO ARQUIVO "web_scraping.py". 
    
    path - URL DO SITE QUE IREI REALIZAR A RASPAGEM DE DADOS
    headers - UTILIZA OS HEADERS DO NAVEGADOR QUE SERÁ UTILIZADO NO SISTEMA PARA SIMULAR UMA REQUISIÇÃO FEITA POR UM NAVEGADOR REAL
    request - A REQUISIÇÃO QUE FOI FEITA
    parsed_html - CONVERTE O FORMATO DOS DADOS REQUISITADOS PARA HTML
    storage_list - DICIONARIO ONDE IREI ARMAZENAR OS DADOS DOS JOGOS CONSULTADOS, ESSES DADOS SERÃO RETORNADOS NA FUNÇÃO E
                    TRATADOS PELAS FUNÇÕES CONTRUIDAS UTILIZANDO A BIBLIOTECA DO DISCORD
    game_list_div - A DIV ONDE FAREI A PESQUISA DOS JOGOS BASEADOS NA CLASSE DO SEU ELEMENTO HTML.
    game_list_elements - TODOS OS ELEMENTOS PRESENTES NA DIV GAME_LIST, TAMBÉM REALIZO A BUSCA BASEADO NA CLASSE HTML 
    game_item - UTILIZANDO O LAÇO DE REPETIÇÃO FOR, EU PERCORRO TODOS OS JOGOS CONSULTADOS E RETORNO DE UM POR UM
    name - NOME DO JOGO
    price - PREÇO DO JOGO
    discount - DESCONTO APLICADO AO PREÇO DO JOGO
    '''    
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


''' ESTA FUNÇÃO AINDA ESTÁ EM DESENVOLVIMENTO! 

    ELA IRÁ CONSULTAR DIARIAMENTE O SITE GG.DEALS UTILIZANDO AS SCHEDULES TASKS DA BIBLIOTECA DO DISCORD E MOSTRARÁ
    AS PROMOÇÕES EM DESTAQUE DAQUELE DIA
    
    data_value - A SESSÃO DE ONDE A FUNÇÃO DO DISCORD IRÁ CONSULTAR AS OFERTAS DIÁRIAS
    path - URL DO SITE QUE IREI REALIZAR A RASPAGEM DE DADOS
    headers - UTILIZA OS HEADERS DO NAVEGADOR QUE SERÁ UTILIZADO NO SISTEMA PARA SIMULAR UMA REQUISIÇÃO FEITA POR UM NAVEGADOR REAL
    request - A REQUISIÇÃO QUE FOI FEITA
    parsed_html - CONVERTE O FORMATO DOS DADOS REQUISITADOS PARA HTML
    storage_list - DICIONARIO ONDE IREI ARMAZENAR OS DADOS DOS JOGOS CONSULTADOS, ESSES DADOS SERÃO RETORNADOS NA FUNÇÃO E
                    TRATADOS PELAS FUNÇÕES CONTRUIDAS UTILIZANDO A BIBLIOTECA DO DISCORD
    game_list_div - A DIV ONDE FAREI A PESQUISA DOS JOGOS BASEADOS NA CLASSE DO SEU ELEMENTO HTML.
    game_list_elements - TODOS OS ELEMENTOS PRESENTES NA DIV GAME_LIST, TAMBÉM REALIZO A BUSCA BASEADO NA CLASSE HTML 
    game_item - UTILIZANDO O LAÇO DE REPETIÇÃO FOR, EU PERCORRO TODOS OS JOGOS CONSULTADOS E RETORNO DE UM POR UM
    name - NOME DO JOGO
    price - PREÇO DO JOGO
    discount - DESCONTO APLICADO AO PREÇO DO JOGO
    '''
def update_daily_deals(data_value): 
     
    path = 'https://gg.deals'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'}
    
    request = requests.get(path, headers=headers)
    parsed_html = BeautifulSoup(request.text, 'html.parser')

    storage_list = {}

    game_list_div = parsed_html.find_all(attrs={"data-preset-name": f"{data_value}"})
    game_list = game_list_div.find('div', class_='list')
    game_list_elements = game_list.find_all('div', class_='game-item')

    for game_item in game_list_elements:
        try:
            name = game_item.find('a', class_='title').get_text()
        except Exception as e:
            print(e)
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