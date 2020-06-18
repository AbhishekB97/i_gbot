import discord
import config
import aiohttp
from discord.ext import commands

bot = commands.Bot(command_prefix='>>', help_command=None, activity=discord.Activity(name='the matrix', type=discord.ActivityType.watching))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if 'bitburner' in message.content.lower():
		await message.channel.send('Bitburner is sooo good!')

	if 'doom' in message.content.lower():
		await message.channel.send('**Dooooooom**')

	await bot.process_commands(message)

@bot.command()
async def help(ctx):
	await ctx.send('''Hi! Thanks for using Shinobot. This is a quirky and sometimes useful bot made by Shinoda. 

Here's its commands:
```>>help - bot info
>>ping - if bot responds, its alive
>>game - bot selects a random game from dSolver's incremental games plaza
>>sing - bot sings shino's favorite incremental game song
>>fav - bot talks about the idle games that Shino remembers fondly```''')

@bot.command()
async def fav(ctx):
	await ctx.send('''Shino has played many incrmental games but some of them stick out in his memory more than others. 

They are (in no particular order):
```Infinite Hero (no longer playable)
Slurpy Derpy (Classic)
Realm Grinder
Zombidle
NGU
Bitburner
	```''')

@bot.command()
async def ping(ctx):
	await ctx.send('pong!')

@bot.command()
async def pong(ctx):
	await ctx.send("That's my line :rolling_eyes:")

@bot.command()
async def sing(ctx):
	await ctx.send('https://timewastinggames.bandcamp.com/track/life-is-a-countdown')

@bot.command()
async def game(ctx):
	async with ctx.channel.typing():
			BASE_API_URL = "https://plaza.dsolver.ca/api/games"
			EMBED_QUERY = '&customFields=slug,name,link,shortDescription,logo'

			async with aiohttp.ClientSession() as session:
				async with session.get(f'{BASE_API_URL}?random=true{EMBED_QUERY}') as resp:
					if resp.status != 200:
						await ctx.send("Something went wrong!  Please try again in a few moments.")
						return
					rand_game, = await resp.json()  # Comma after rand_game to get unpack the list and get the dict
				await ctx.send(f'{ctx.author.mention} Try {rand_game["link"]}')

bot.run(config.TOKEN)