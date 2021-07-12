import os
from discord.embeds import Embed
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
    try:
        status = await getWins(arg1, arg2, arg3)

        if status == None:
            await ctx.send(f'{arg1} and {arg2} haven\'t played together in {arg1}s {arg3} latest games')
        else:    
            playerOneCount = status.get('playerOneCount', 0)
            playerTwoCount = status.get('playerTwoCount', 0)
            sameAmount = status.get('sameAmount', 0)

            embed=Embed(title=f'{arg1} vs {arg2}', description=f'Who had most kills over {arg3} games?', color=0x0004ff)
            embed.add_field(name=f'{arg1}', value=f'{playerOneCount} wins', inline=True)
            embed.add_field(name=f'{arg2}', value=f'{playerTwoCount} wins', inline=True)

            if(sameAmount != 0):
                embed.set_footer(text = f'Same amount of kills in {sameAmount} game(s)')

            await ctx.send(embed=embed)
    except ValueError as err:
        await ctx.send(f'Failed with error: {err.args}')
            
bot.run(TOKEN)