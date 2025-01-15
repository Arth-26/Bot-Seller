import discord
from discord.ext import commands, tasks
import os
from classes.selenium_functions import DealBot
from classes.web_scraping import ScrapingBot

token = str(os.getenv('BOT_TOKEN')) # TOKEN DE API DO DISCORD

# Variável de configuração usada para a comunicação com o gateway
intents = discord.Intents.all()

# Variável de eventos usada para realizar os comandos. Usada como tag nas funções que serão usadas no discord
bot = commands.Bot(command_prefix="!", intents=intents)

""" EVENTOS DE INICIAÇÃO """

""" EVENTO ATIVADOS QUANDO O BOT ENTRA NO SERVIDOR """
@bot.event
async def on_guild_join(guild):
    # Cria um canal de texto no servidor
    channel = await guild.create_text_channel('promoções')

    # Altera as permissões para o canal
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=True),  # Remover permissão de envio de mensagens, mas permitir reações
        bot.user: discord.PermissionOverwrite(send_messages=True),  # Permitir que o bot envie mensagens
    }
    
    # Permissões para o dono do servidor (ele pode enviar mensagens)
    owner = guild.owner
    if owner:
        overwrites[owner] = discord.PermissionOverwrite(send_messages=True, add_reactions=True)  # Permite que o dono envie mensagens e reaja

    # Atualizar permissões do canal
    await channel.edit(overwrites=overwrites)
    

    canal_criado_id = channel.id # ID do canal criado para ser usado na função de atualizações periodicas de promoções
    daily_games_update.start(canal_criado_id)
    print(f'Canal {channel.name} criado com sucesso no servidor {guild.name}')

""" EVENTO REALIZANDO ASSIM QUE O BOT ESTÁ PRONTO PARA USO """
@bot.event
async def on_ready():
    # Envia uma mensagem ao console para indicar que está pronto
    print('Estou funcionando! Pode começar a usar nossos comandos!')


""" DEALS FUNCTIONS """

""" EVENTO QUE BUSCA OS JOGOS EM DESTAQUE DA SESSÃO DE JOGOS POPULARES """
@bot.command(name='popularGames')
async def populargames(message):
    await message.send('Espere um pouco, estamos processando!')

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.see_popular_games()

    # Formatação dos jogos
    # Cada página mostrará 10 jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}' # Formatação das informações dos jogos exibido na lista 
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)  # Caso falte jogos para completar a ultima página, adiciona ela a lista como uma pagina incompleta mesmo

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Jogos Populares - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/games/)') # Link para que o usuário possa acessar a página do site 
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação de páginas
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    # Verifica se quem está tentando navegar nas páginas é quem iniciou a função
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            # O bot espera por interações na navegação de página durante 1 minuto, após isso, ele encerra o evento
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            # Verifica a ação e navega pelas páginas
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
            # Ao encerrar o evento de navegação de páginas, ele envia um EMBED ao servidor avisando o encerramento
            embed_error = discord.Embed(
                title=f'Jogos Populates - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

""" EVENTO QUE BUSCA OS JOGOS EM DESTAQUE DA SESSÃO DE MELHORES OFERTAS """
@bot.command(name='bestDeals')
async def best_deals(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.see_best_deals()
    
    # Formatação dos jogos
    # Cada página mostrará 10 jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}' # Formatação das informações dos jogos exibido na lista 
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)   # Caso falte jogos para completar a ultima página, adiciona ela a lista como uma pagina incompleta mesmo

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Melhores Promoções - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/deals/)') # Link para que o usuário possa acessar a página do site 
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação de páginas
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    # Verifica se quem está tentando navegar nas páginas é quem iniciou a função
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            # O bot espera por interações na navegação de página durante 1 minuto, após isso, ele encerra o evento
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            # Verifica a ação e navega pelas páginas
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
            # Ao encerrar o evento de navegação de páginas, ele envia um EMBED ao servidor avisando o encerramento
            embed_error = discord.Embed(
                title=f'Melhores Promoções - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

""" EVENTO QUE BUSCA OS JOGOS EM DESTAQUE DA SESSÃO DE JOGOS GRÁTIS """
@bot.command(name='freeGames')
async def free_games(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.see_free_games()
    
    # Formatação dos jogos
    # Cada página mostrará 10 jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}' # Formatação das informações dos jogos exibido na lista 
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)   # Caso falte jogos para completar a ultima página, adiciona ela a lista como uma pagina incompleta mesmo

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Jogos Gratuitos - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/games/?maxPrice=0&sort=wanted)') # Link para que o usuário possa acessar a página do site 
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação de páginas
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    # Verifica se quem está tentando navegar nas páginas é quem iniciou a função
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            # O bot espera por interações na navegação de página durante 1 minuto, após isso, ele encerra o evento
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            # Verifica a ação e navega pelas páginas
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
            # Ao encerrar o evento de navegação de páginas, ele envia um EMBED ao servidor avisando o encerramento
            embed_error = discord.Embed(
                title=f'Jogos Gratuitos - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

""" EVENTO QUE BUSCA OS JOGOS EM DESTAQUE DA SESSÃO DE NOVAS OFERTAS """
@bot.command(name='newDeals')
async def new_deals(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.see_new_deals()
    
    # Formatação dos jogos
    # Cada página mostrará 10 jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}' # Formatação das informações dos jogos exibido na lista 
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)   # Caso falte jogos para completar a ultima página, adiciona ela a lista como uma pagina incompleta mesmo

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Novas Ofertas - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/deals/new-deals/)') # Link para que o usuário possa acessar a página do site 
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação de páginas
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    # Verifica se quem está tentando navegar nas páginas é quem iniciou a função
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            # O bot espera por interações na navegação de página durante 1 minuto, após isso, ele encerra o evento
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            # Verifica a ação e navega pelas páginas
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
            # Ao encerrar o evento de navegação de páginas, ele envia um EMBED ao servidor avisando o encerramento
            embed_error = discord.Embed(
                title=f'Novas Ofertas - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

""" EVENTO QUE BUSCA OS JOGOS EM DESTAQUE DA SESSÃO DE OFERTAS COM MENORES PREÇOS HISTÓRICOS """
@bot.command(name='historicalLow')
async def historical_low(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.see_game_historical_low()
    
    # Formatação dos jogos
    # Cada página mostrará 10 jogos
    paginas = []
    pagina_atual = []
    for game, info in games.items():
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}' # Formatação das informações dos jogos exibido na lista 
        pagina_atual.append(display_message)
        if len(pagina_atual) == 10:
            paginas.append(pagina_atual)
            pagina_atual = []
    if pagina_atual:
        paginas.append(pagina_atual)   # Caso falte jogos para completar a ultima página, adiciona ela a lista como uma pagina incompleta mesmo

    # Criação do Embed inicial
    indice = 0
    embed = discord.Embed(
        title=f'Baixa Histórica - Página {indice + 1}/{len(paginas)}',
        description='\n'.join(paginas[indice]),
        color=discord.Color.blue()
    )
    embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals/deals/historical-lows/)') # Link para que o usuário possa acessar a página do site 
    mensagem = await message.send(embed=embed)

    # Adiciona as reações para navegação de páginas
    for emoji in ['⬅️', '➡️']:
        await mensagem.add_reaction(emoji)

    # Verifica se quem está tentando navegar nas páginas é quem iniciou a função
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == mensagem.id

    # Controle de Paginação
    while True:
        try:
            # O bot espera por interações na navegação de página durante 1 minuto, após isso, ele encerra o evento
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            # Verifica a ação e navega pelas páginas
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
            # Ao encerrar o evento de navegação de páginas, ele envia um EMBED ao servidor avisando o encerramento
            embed_error = discord.Embed(
                title=f'Baixa Histórica - Tempo Esgotado',
                description='Para acessar a lista, execute o comando novamente',
                color=discord.Color.brand_red()
            )
            await message.send(embed=embed_error)
            break

    
""" SCHEDULE TASKS """

""" EVENTO QUE ENVIA PERIODICAMENTE LISTA COM OS PRINCIPAIS JOGOS DE CADA SESSÃO """
@tasks.loop(hours=8)
async def daily_games_update(canal):

    # Simulação de scraping
    scraping_bot = ScrapingBot()
    games = scraping_bot.daily_games_update()

    # Seleciona o canal do discord onde serão enviadas os EMBEDS com a lista de jogos
    channel = bot.get_channel(canal)
    
    # Cada sessão de jogos acessada enviará um EMBED com 10 jogos na lista para o canal definido
    for session, games_info in games.items():
        pagina = []
        for game, info in games_info.items():
            for price, discount in info.items():
                display_message = f'{game}: {price} | {discount}' # Formatação das informações dos jogos exibido na lista
            pagina.append(display_message)
        
        embed = discord.Embed(
            title=f'{session}',
            description='\n'.join(pagina),
            color=discord.Color.blue()
        )
        embed.add_field(name='Mais informações:', value='[Clique aqui](https://gg.deals)') # Link para que o usuário possa acessar a página do site 
        await channel.send(embed=embed)


bot.run(token)
