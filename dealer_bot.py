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
tasks_by_guild = {}  # Dicionário para armazenar tarefas por ID do servidor, assim, verifica se a mesma tarefa não será iniciada mais de uma vez

""" EVENTOS DE INICIAÇÃO """

""" EVENTO ATIVADOS QUANDO O BOT ENTRA NO SERVIDOR """
@bot.event
async def on_guild_join(guild):
    # Cria um canal de texto no servidor

    channel = discord.utils.get(guild.text_channels, name="promoções")
    if not channel:
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
    
    # Inicia as tasks diárias usando o id do servidor e do canal onde será enviada as mensagens do evento
    start_daily_task(guild.id, channel.id)
    print(f'Canal {channel.name} criado com sucesso no servidor {guild.name}')

""" EVENTO REALIZANDO ASSIM QUE O BOT ESTÁ PRONTO PARA USO """
@bot.event
async def on_ready():

    # Mostra o comando de ajuda no perfil do bot
    activity = discord.Game(name="For more info: !help_me")
    await bot.change_presence(activity=activity)

    # Envia uma mensagem ao console para indicar que está pronto
    print('Estou funcionando! Pode começar a usar nossos comandos!')

    # Verifica todos os servidores que o bot está presente e reativa a função de atualiações diárias junto com o bot
    for guild in bot.guilds:
        promo_channel = discord.utils.get(guild.text_channels, name="promoções")
        if promo_channel:
            try:
                start_daily_task(guild.id, promo_channel.id)
            except:
                print('Já está rodando neste servidor')


""" FUNÇÕES BASE """

@bot.command(name="help_me", description="Mostra a lista de comandos.")
async def command_list(message):
    comandos = {
        '!popular_games': 'Mostra a lista de jogos populares em promoção.', 
        '!best_deals': 'Mostra a lista das melhores promoções do dia.', 
        '!free_games': 'Mostra a lista de jogos que são ou estão gratuitos.', 
        '!new_deals': 'Mostra a lista de novas promoções.', 
        '!historical_low': 'Mostra a lista de jogos com preços com baixa histórica.'
        }
    
    # Construir a string com os comandos e descrições
    descricao_comandos = '\n'.join([f'**{comando}** - {descricao}' for comando, descricao in comandos.items()])
    
    embed = discord.Embed(
        title='LISTA DE COMANDOS',
        description=descricao_comandos,
        color=discord.Color.blue()
    )

    mensagem = await message.send(embed=embed)


""" DEALS FUNCTIONS """

""" EVENTO QUE BUSCA OS JOGOS EM DESTAQUE DA SESSÃO DE JOGOS POPULARES """

@bot.command(name="popular_games", description="Mostra a lista de jogos populares em promoção.")
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
@bot.command(name="best_deals", description="Mostra a lista das melhores promoções do dia.")
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
@bot.command(name="free_games", description="Mostra a lista de jogos que são ou estão gratuitos.")
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
@bot.command(name="new_deals", description="Mostra a lista de novas promoções.")
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
@bot.command(name="historical_low", description="Mostra a lista de jogos com preços com baixa histórica.")
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


""" ANTES, A FUNÇÃO daily_games_update() ERA CHAMADA INDIVIDUALMENTE, SEM A NECESSIDADE DE UMA FUNÇÃO PAI
PORÉM, A TAG @tasks.loop DO DISCORD TEM A LIMITAÇÃO DE NÃO CONSEGUIR IDENTIFICAR QUE ESTÁ SENDO INICIADA EM SERVIDORES
DIFERENTES, ELA É INICIADA EM UM ESCOPO GLOBAL DO SISTEMA, ENTÃO, LIMITEI O ESCOPO DELA DENTRO DA FUNÇÃO start_daily_task().
A FUNÇÃO POSSUI UMA VERIFICAÇÃO PARA EVITAR QUE SEJA ATIVADA DUAS VEZES NO MESMO SERVIDOR E EVITAR ERROS."""

""" EVENTO QUE ENVIA PERIODICAMENTE LISTA COM OS PRINCIPAIS JOGOS DE CADA SESSÃO """
# Função para criar uma tarefa de atualização para um canal
def start_daily_task(guild_id, channel_id):
    if guild_id in tasks_by_guild:  # Verifica se a tarefa já existe
        print(f"Tarefa já em execução para o servidor {guild_id}")
        return
    
    @tasks.loop(hours=8)
    async def daily_games_update():

        # Simulação de scraping
        scraping_bot = ScrapingBot()
        games = scraping_bot.daily_games_update()

        # Seleciona o canal do discord onde serão enviadas os EMBEDS com a lista de jogos
        channel = bot.get_channel(channel_id)
        
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
    
    # Inicia a task
    daily_games_update.start()
    tasks_by_guild[guild_id] = daily_games_update  # Salva a tarefa no dicionário para evitar iniciar novamente no mesmo servidor

bot.run(token)
