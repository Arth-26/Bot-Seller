import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from classes.selenium_functions import DealBot
from classes.web_scraping import ScrapingBot

load_dotenv()

token = str(os.getenv('BOT_TOKEN'))


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


""" DEALS FUNCTIONS """

@bot.event
async def on_ready():
    print('Estou funcionando! Pode começar a usar nossos comandos!')

@bot.command(name='popularGames')
async def populargames(message):
    await message.send('Espere um pouco, estamos processando!')

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.see_popular_games()

    # Formatação dos jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}'
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)  # Adiciona a última página, se tiver sobras

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Jogos Populares - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/games/)')
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == '➡️' and indice < len(paginas) - 1:
                indice += 1
            elif reaction.emoji == '⬅️' and indice > 0:
                indice -= 1

            embed.title = f'Jogos Populares - Página {indice + 1}/{len(paginas)}'
            embed.description = '\n'.join(paginas[indice])
            await mensagem.edit(embed=embed)
            await mensagem.clear_reactions()
            for emoji in ['⬅️', '➡️']:
                await mensagem.add_reaction(emoji)
        except TimeoutError:
            embed_error = discord.Embed(
                title=f'Jogos Populates - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

@bot.command(name='bestDeals')
async def best_deals(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    scraping_bot = ScrapingBot()
    games = scraping_bot.see_best_deals()
    
    # Formatação dos jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}'
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)  # Adiciona a última página, se tiver sobras

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Melhores Promoções - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/deals/)')
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == '➡️' and indice < len(paginas) - 1:
                indice += 1
            elif reaction.emoji == '⬅️' and indice > 0:
                indice -= 1

            embed.title = f'Melhores Promoções - Página {indice + 1}/{len(paginas)}'
            embed.description = '\n'.join(paginas[indice])
            await mensagem.edit(embed=embed)
            await mensagem.clear_reactions()
            for emoji in ['⬅️', '➡️']:
                await mensagem.add_reaction(emoji)
        except TimeoutError:
            embed_error = discord.Embed(
                title=f'Melhores Promoções - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

@bot.command(name='freeGames')
async def free_games(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    scraping_bot = ScrapingBot()
    games = scraping_bot.see_free_games()
    
    # Formatação dos jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}'
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)  # Adiciona a última página, se tiver sobras

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Jogos Gratuitos - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/games/?maxPrice=0&sort=wanted)')
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == '➡️' and indice < len(paginas) - 1:
                indice += 1
            elif reaction.emoji == '⬅️' and indice > 0:
                indice -= 1

            embed.title = f'Jogos Gratuitos - Página {indice + 1}/{len(paginas)}'
            embed.description = '\n'.join(paginas[indice])
            await mensagem.edit(embed=embed)
            await mensagem.clear_reactions()
            for emoji in ['⬅️', '➡️']:
                await mensagem.add_reaction(emoji)
        except TimeoutError:
            embed_error = discord.Embed(
                title=f'Jogos Gratuitos - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

@bot.command(name='newDeals')
async def new_deals(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    scraping_bot = ScrapingBot()
    games = scraping_bot.see_new_deals()
    
    # Formatação dos jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}'
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)  # Adiciona a última página, se tiver sobras

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Novas Ofertas - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/deals/new-deals/)')
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == '➡️' and indice < len(paginas) - 1:
                indice += 1
            elif reaction.emoji == '⬅️' and indice > 0:
                indice -= 1

            embed.title = f'Novas Ofertas - Página {indice + 1}/{len(paginas)}'
            embed.description = '\n'.join(paginas[indice])
            await mensagem.edit(embed=embed)
            await mensagem.clear_reactions()
            for emoji in ['⬅️', '➡️']:
                await mensagem.add_reaction(emoji)
        except TimeoutError:
            embed_error = discord.Embed(
                title=f'Novas Ofertas - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

@bot.command(name='historicalLow')
async def historical_low(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    scraping_bot = ScrapingBot()
    games = scraping_bot.see_game_historical_low()
    
    # Formatação dos jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}'
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)  # Adiciona a última página, se tiver sobras

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Baixa Histórica - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/deals/historical-lows/)')
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == '➡️' and indice < len(paginas) - 1:
                indice += 1
            elif reaction.emoji == '⬅️' and indice > 0:
                indice -= 1

            embed.title = f'Baixa Histórica - Página {indice + 1}/{len(paginas)}'
            embed.description = '\n'.join(paginas[indice])
            await mensagem.edit(embed=embed)
            await mensagem.clear_reactions()
            for emoji in ['⬅️', '➡️']:
                await mensagem.add_reaction(emoji)
        except TimeoutError:
            embed_error = discord.Embed(
                title=f'Baixa Histórica - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

    

""" NEWS FUNCTIONS """

@bot.command(name='dailyNews')
async def daily_news(message):
    pass


bot.run(token)
