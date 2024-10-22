import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from bot_functions import DealBot

load_dotenv()

token = str(os.getenv('BOT_TOKEN'))


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Estou funcionando! Pode começar a usar nossos comandos!')

@bot.command(name='popularGames')
async def popular_games(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    deal_bot = DealBot()
    games = deal_bot.see_popular_games()
    count = 0
    game_list = ''

    for game, info in games.items():
        if count == 10:
            await message.channel.send(game_list)
            await message.channel.send('-------------------------------------------------------------')
            game_list = ''
            count = 0
        for price, discount in info.items():
            display_message = f'{game}: {price} | {discount}'
        game_list += f'{display_message}\n'
        count += 1
    await message.channel.send(game_list)


bot.run(token)
