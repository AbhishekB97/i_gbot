import discord
import config
import aiohttp
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix='>>', help_command=None, activity=discord.Activity(name='the matrix', type=discord.ActivityType.watching))
channel_name = ""

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if(channel_name == "" or message.channel.id == discord.utils.get(message.guild.channels, name=channel_name).id):
		await bot.process_commands(message)

@bot.command(name="help",pass_context=True)
async def _help(ctx):
	await ctx.send('''Hi! Thanks for using Shinobot. This is a quirky and sometimes useful bot made by Shinoda. 

Here's its commands:
```>>help - bot info
>>ping - if bot responds, its alive
>>game <n> - bot selects n mod 10 distinct random games from dSolver's incremental games plaza
>>sing - bot sings shino's favorite incremental game song
>>set_channel - bot will make this channel its forever home and not speak outside this channel
>>fav - bot talks about the idle games that Shino remembers fondly```''')

@bot.command(name="fav",pass_context=True)
async def _fav(ctx):
	await ctx.send('''Shino has played many incrmental games but some of them stick out in his memory more than others. 

They are (in no particular order):
```Infinite Hero (no longer playable)
Slurpy Derpy (Classic)
Realm Grinder
Zombidle (RIP)
NGU
Bitburner
	```''')

@bot.command(name="set_channel",pass_context=True)
@has_permissions(manage_channels=True)
async def _set_channel(ctx, name):
	global channel_name
	channel_name = name
	await ctx.send(f'Shinobot has made #{name} its forever home!')

@_set_channel.error
async def _set_channel_error(ctx,error):
	if isinstance(error, MissingPermissions):
		text = f"Sorry {ctx.author.mention}, you do not have permissions to do that!".format(ctx.message.author)
		await ctx.send(text)

@bot.command(name="ping",pass_context=True)
async def _ping(ctx):
	await ctx.send('pong!')

@bot.command(name="pong",pass_context=True)
async def _pong(ctx):
	await ctx.send("That's my line :rolling_eyes:")

@bot.command(name="sing",pass_context=True)
async def _sing(ctx):
	await ctx.send('https://timewastinggames.bandcamp.com/track/life-is-a-countdown')

@bot.command(name="game",pass_context=True)
async def _game(ctx, n='1'):
	async with ctx.channel.typing():
		BASE_API_URL = "https://plaza.dsolver.ca/api/games"
		EMBED_QUERY = '&customFields=slug,name,link,shortDescription,logo'

		if not n.isdigit():
			await ctx.send(f'{ctx.author.mention} I cant count {n} games...')
			return

		async with aiohttp.ClientSession() as session:
			linkset = set()
			while len(linkset) < int(n) % 10:
				async with session.get(f'{BASE_API_URL}?random=true{EMBED_QUERY}') as resp:
					if resp.status != 200:
						await ctx.send("Something went wrong!  Please try again in a few moments.")
						return
					rand_game, = await resp.json()  # Comma after rand_game to get unpack the list and get the dict
					link = rand_game['link']
					linkset.add(link)
			linkstr = '\n'.join(linkset)
			await ctx.send(f"{ctx.author.mention} Try: \n{linkstr}")

bot.run(config.TOKEN)