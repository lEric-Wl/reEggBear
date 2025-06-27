import discord

import json
import os
from os.path import exists

with open('creds.json','r') as saves:
		creds = json.load(saves)
		saves.close()

discordToken = creds['discordToken']

intent = discord.Intents.all()
bot = discord.Bot(intents = intent)
allCogs = ['lottery','econ']

@bot.event
async def on_ready():
	print("Ready\n----------------------------")
	if not exists('saves.json'):
		with open('saves.json','w') as saves:
			json.dump({'members': {"0":[0,0]}},saves,indent=4)
			saves.close()
	
@bot.command(description = 'Not for you to use')
async def reload(ctx, extension = None):
	#Reloads all of the cogs so that the bot does not need to be rebooted to update the code
	
	await ctx.defer(ephemeral = True);
	
	if not await bot.is_owner(ctx.author):
		await ctx.respond('I told you in the description this is not for you to use, you Dingus!')
		return
	
	try:
		if extension is not None:
			bot.reload_extension(f'cogs.{extension}')
		else:
			for stuff in allCogs:
				bot.reload_extension(f'cogs.{stuff}')
		print("\n\n\n\n\n\n\n\n\n\nreloaded")
		
		await ctx.respond('Done',ephemeral = True)
		
	except discord.ExtensionError as e:
		await ctx.respond(f"Error: {str(e)}", ephemeral=True)	
	except Exception as e:
		await ctx.respond(f"Unexpected error: {str(e)}", ephemeral=True)
  
@bot.command()
async def ping(ctx):
	await ctx.respond(f"Pong! Latency is {bot.latency}")
	print("recived")

for stuff in allCogs:
	bot.load_extension(f'cogs.{stuff}')	
	
bot.run(discordToken)

