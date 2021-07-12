import os
import logging
from discord.embeds import Embed
from discord.ext import commands
from dotenv import load_dotenv
from faceit_service import getWins

load_dotenv()
logging.basicConfig(encoding='utf-8', level=logging.INFO)

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logging.error('DISCORD_TOKEN is empty')

bot = commands.Bot(command_prefix='!')
logging.info('Sat bot prefix to !')

@bot.event
async def on_ready():
    logging.info(f'{bot.user.name} has connected to Discord!\n')
    active_guilds = bot.guilds
    for guild in active_guilds:
        logging.info(f'Talking in {guild.name}\n')

@bot.command(name='faceit', help='.!faceit <NICK1> <NICK2> <X-GAMES>')
async def faceitChecker(ctx, arg1, arg2, arg3 = 10):
    if arg3 > 200:
        arg3 == 200

    try:
        logging.info(f'{ctx.author.name} called !faceit command')
        status = await getWins(arg1, arg2, arg3)

        if status == None:
            await ctx.send(f'{arg1} and {arg2} haven\'t played together in {arg1}s {arg3} latest games')
        else:    
            inSameLobby = status.get('inSameLobby', 0)
            playerOneCount = status.get('playerOneCount', 0)
            playerTwoCount = status.get('playerTwoCount', 0)
            sameAmount = status.get('sameAmount', 0)

            embed=Embed(title=f'{arg1} vs {arg2}', description=f'You played together {inSameLobby} time(s) in the last {arg3} game(s)', color=0x0004ff)
            embed.add_field(name=f'{arg1}', value=f'{playerOneCount} wins', inline=True)
            embed.add_field(name=f'{arg2}', value=f'{playerTwoCount} wins', inline=True)

            if(sameAmount != 0):
                embed.set_footer(text = f'Same amount of kills in {sameAmount} game(s)')

            await ctx.send(embed=embed)
    except ValueError as err:
        logging.error('Failed with error: {}'.format(err.args))
        await ctx.send(f'Failed with error: {err.args}')

@faceitChecker.error
async def faceitChecker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing some arguments')
            
bot.run(TOKEN)