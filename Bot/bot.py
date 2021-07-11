import os
from discord.ext import commands
from dotenv import load_dotenv
from faceit_service import getWins

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!\n')
    active_guilds = bot.guilds
    for guild in active_guilds:
        print(f'Talking in {guild.name}\n')

@bot.command(name='faceit', help='Compare kills between to users when they play together')
async def faceitChecker(ctx, arg1, arg2, arg3 = 10):
    status = await getWins(arg1, arg2, arg3)
    await ctx.send(status)
            
bot.run(TOKEN)