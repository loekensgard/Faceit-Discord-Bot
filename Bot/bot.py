import logging
from discord.embeds import Embed
from discord.ext import commands
from config import settings
from faceit_service import get_stats

from error_extensions import NeverInSameLobbyError
from player_stats_class import player_stats

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

@bot.command(name='faceitstats', aliases = ['fstats'] , help='.!fstats <NICK1> <NICK2> <X-GAMES>')
async def faceit_check_kills(ctx, arg1, arg2, arg3 = 10):
    if arg3 > 100:
        arg3 == 100

    try:
        logging.info(f'{ctx.author.name} called !faceit command')
        in_same_lobby, player1, player2 = await get_stats(arg1, arg2, arg3)

        await ctx.send(embed=create_embed(in_same_lobby,player1,player2,arg3))
    except NeverInSameLobbyError as err:
        await ctx.send(f'{arg1} and {arg2} haven\'t played together in {arg1}s {arg3} latest games')
    except ValueError as err:
        logging.error('Failed with error: {}'.format(err.args))
        await ctx.send(f'Failed with error: {err.args}')

@faceit_check_kills.error
async def faceit_checker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing some arguments')


def create_embed(in_same_lobby, player1, player2, inputGames):

    embed=Embed(
        title=f'{player1.name} vs {player2.name}', 
        description=f'You played together {in_same_lobby} time(s) in the last {inputGames} game(s)\n\n\
        {player1.name} had most:\n**Kills**: {player1.kills} time(s)\n**Deaths**: {player1.deaths} time(s)\n**Hs**: {player1.hs} time(s)\n\n\
        {player2.name} had most:\n**Kills**: {player2.kills} time(s)\n**Deaths**: {player2.deaths} time(s)\n**Hs**: {player2.hs} time(s)\n\n', color=0xFF5500)
    if player1.avatar is not None:    
        embed.set_thumbnail(url=player1.avatar)

    if player1.same_amount_kills != 0:
        embed.description += f'*Same amount kills*: {player1.same_amount_kills} time(s)\n'
    if player1.same_amount_deaths != 0:
        embed.description += f'*Same amount deaths*: {player1.same_amount_deaths} time(s)\n'    
    if player1.same_amount_hs != 0:
        embed.description += f'*Same amount hs*: {player1.same_amount_hs} time(s)\n'
    return embed
            
bot.run(TOKEN)