import discord
import config
import aiohttp

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(name='my dudes', type=discord.ActivityType.watching))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('>>ping'):
		await message.channel.send('pong!')

	if 'bitburner' in message.content:
		await message.channel.send('Bitburner is sooo good!')

	'''if '4G' in message.content:
		await message.add_reaction(emoji='\U0000FE0F')
		await message.add_reaction(emoji='\U0001F1EC')'''

	if message.content.startswith('>>song'):
		await message.channel.send('https://timewastinggames.bandcamp.com/album/suicidle-ost')

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