from inspect import CO_OPTIMIZED
import os
import discord
from discord.ext import commands
from discord.guild import Guild
from dotenv import load_dotenv
from faceit_service import getWins, getPlayerId

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user.name} has connected to Discord!\n'
        f'Talking in {guild.name}'
        )

@bot.command(name='faceit', help='Compare kills between to users when they play together')
async def faceitChecker(ctx, arg1, arg2, arg3 = 10):
    status = await getWins(arg1, arg2, arg3)
    await ctx.send(status)
            
bot.run(TOKEN)