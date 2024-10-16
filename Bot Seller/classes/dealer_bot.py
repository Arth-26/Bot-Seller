import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from bot_functions import DealBot

load_dotenv()

token = str(os.getenv('BOT_TOKEN'))


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Hello World')


@bot.command(name='waiting')
async def wait_a_second(ctx):
    await ctx.send('Espere um pouco, estamos processando!')

@bot.command(name='popularGames')
async def popular_games(message):
    await message.channel.send('Espere um pouco, estamos processando!')

    deal_bot = DealBot()
    games = deal_bot.see_popular_games()
    contador = 0

    for game, info in games.items():
        if contador == 5:
            break
        for price, discount in info.items():
            await message.channel.send(f'{game}: {price} | {discount}')
        contador += 1



bot.run(token)
