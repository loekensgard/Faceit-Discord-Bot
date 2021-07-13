import logging
from discord.embeds import Embed
from discord.ext import commands
from config import settings
from faceit_service import getWins

logging.basicConfig(encoding='utf-8', level=logging.INFO)

TOKEN = settings.TOKEN
if not TOKEN: logging.error('DISCORD_TOKEN is empty')

bot = commands.Bot(command_prefix='!')
logging.info('Sat bot prefix to !')

@bot.event
async def on_ready():
    logging.info(f'{bot.user.name} has connected to Discord!\n')
    active_guilds = bot.guilds
    for guild in active_guilds:
        logging.info(f'Talking in {guild.name}\n')

@bot.command(name='faceitkills', aliases = ['fkills'] , help='.!fkills <NICK1> <NICK2> <X-GAMES>')
async def faceit_check_kills(ctx, arg1, arg2, arg3 = 10):
    if arg3 > 100:
        arg3 == 100

    try:
        logging.info(f'{ctx.author.name} called !faceit command')
        status = await getWins(arg1, arg2, arg3, 'Kills')

        if status == None:
            await ctx.send(f'{arg1} and {arg2} haven\'t played together in {arg1}s {arg3} latest games')
        else:
            await ctx.send(embed=create_embed(status,arg1,arg2,arg3, 'Kills'))
    except ValueError as err:
        logging.error('Failed with error: {}'.format(err.args))
        await ctx.send(f'Failed with error: {err.args}')

@bot.command(name='faceitdeath', aliases = ['fdeath'], help='.!fdeath <NICK1> <NICK2> <X-GAMES>')
async def faceit_check_death(ctx, arg1, arg2, arg3 = 10):
    if arg3 > 200:
        arg3 == 200

    try:
        logging.info(f'{ctx.author.name} called !faceit command')
        status = await getWins(arg1, arg2, arg3, 'Deaths')

        if status == None:
            await ctx.send(f'{arg1} and {arg2} haven\'t played together in {arg1}s {arg3} latest games')
        else:
            await ctx.send(embed=create_embed(status,arg1,arg2,arg3, 'Deaths'))
    except ValueError as err:
        logging.error('Failed with error: {}'.format(err.args))
        await ctx.send(f'Failed with error: {err.args}')

@bot.command(name='faceiths', aliases = ['fhs'], help='.!fhs <NICK1> <NICK2> <X-GAMES>')
async def faceit_check_hs(ctx, arg1, arg2, arg3 = 10):
    if arg3 > 200:
        arg3 == 200

    try:
        logging.info(f'{ctx.author.name} called !faceit command')
        status = await getWins(arg1, arg2, arg3, 'Headshots %')

        if status == None:
            await ctx.send(f'{arg1} and {arg2} haven\'t played together in {arg1}s {arg3} latest games')
        else:
            await ctx.send(embed=create_embed(status,arg1,arg2,arg3, 'Headshots %'))
    except ValueError as err:
        logging.error('Failed with error: {}'.format(err.args))
        await ctx.send(f'Failed with error: {err.args}')

@faceit_check_kills.error
async def faceit_checker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing some arguments')

@faceit_check_death.error
async def faceit_hecker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing some arguments')

@faceit_check_hs.error
async def faceit_checker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing some arguments')

def create_embed(status, player1, player2, inputGames, property):
    inSameLobby = status.get('inSameLobby', 0)
    playerOneCount = status.get('playerOneCount', 0)
    playerTwoCount = status.get('playerTwoCount', 0)
    sameAmount = status.get('sameAmount', 0)

    embed=Embed(title=f'{player1} vs {player2}', description=f'You played together {inSameLobby} time(s) in the last {inputGames} game(s)', color=0xFF5500)
    embed.add_field(name=f'{player1}', value=f'{playerOneCount} wins', inline=True)
    embed.add_field(name=f'{player2}', value=f'{playerTwoCount} wins', inline=True)

    if(sameAmount != 0):
        embed.set_footer(text = f'Same amount of {property} in {sameAmount} game(s)')     
    return embed   
            
bot.run(TOKEN)