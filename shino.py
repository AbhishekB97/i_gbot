import discord
import config
import aiohttp

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(name='the matrix', type=discord.ActivityType.watching))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('>>help'):
		await message.channel.send('''Hi! Thanks for using Shinobot. This is a quirky and sometimes useful bot made by Shinoda. 

Here's its commands:
```>>help - bot info
>>ping - if bot responds, its alive
>>game - bot selects a random game from dSolver's incremental games plaza
>>sing - bot sings shino's favorite incremental game song
>>fav - bot talks about the idle games that Shino remembers fondly```''')

	if message.content.startswith('>>ping'):
		await message.channel.send('pong!')

	if 'bitburner' in message.content.lower():
		await message.channel.send('Bitburner is sooo good!')

	if message.content.startswith(">>fav"):
		await message.channel.send('''Shino has played many incrmental games but some of them stick out in his memory more than others. 

They are (in no particular order):
```Infinite Hero (no longer playable)
Slurpy Derpy (Classic)
Realm Grinder
Zombidle
NGU
Bitburner
	```''')

	if message.content.startswith('>>sing'):
		await message.channel.send('https://timewastinggames.bandcamp.com/track/life-is-a-countdown')

	if message.content.startswith('>>game'):
		async with message.channel.typing():
			BASE_API_URL = "https://plaza.dsolver.ca/api/games"
			EMBED_QUERY = '&customFields=slug,name,link,shortDescription,logo'

			async with aiohttp.ClientSession() as session:
				async with session.get(f'{BASE_API_URL}?random=true{EMBED_QUERY}') as resp:
					if resp.status != 200:
						await message.channel.send("Something went wrong!  Please try again in a few moments.")
						return
					rand_game, = await resp.json()  # Comma after rand_game to get unpack the list and get the dict
				await message.channel.send(f'{message.author.mention} Try {rand_game["link"]}')

client.run(config.TOKEN)