import discord
import json
import os
from os.path import exists

if not exists('saves.json'):
    with open('saves.json', 'w') as saves:
        json.dump({'members': {}, 'lottery': {},'timer':{"daily":{},"dne":{}},'dne':{}}, saves, indent=4)

with open('creds.json', 'r') as creds_file:
    creds = json.load(creds_file)

discordToken = creds['discordToken']

intent = discord.Intents.all()
bot = discord.Bot(intents=intent)
allCogs = ['lottery', 'econ', 'dne']

@bot.event
async def on_ready():
    print("Ready\n----------------------------")

class FileManager:
    def __init__(self, bot=None):
        self.saves_file = 'saves.json'
        self.saves = None
        self.bot = bot
        self.load_saves()
        
    def load_saves(self):
        with open(self.saves_file, 'r') as saves:
            self.saves = json.load(saves)

    def save_saves(self):
        with open(self.saves_file, 'w') as saves:
            json.dump(self.saves, saves, indent=4)
        self.load_saves()

    def add_member(self, memberId):
        if memberId not in self.saves['members']:
            self.saves['members'][memberId] = [0, 0] # Holding, Bank
            self.save_saves()

    def check_member(self, memberId):
        self.load_saves()
        if self.bot:
            user = self.bot.get_user(int(memberId))
            if user is None or user.bot:
                return 
        if memberId not in self.saves['members']:
            self.add_member(memberId)

bot.file_manager = FileManager(bot)

@bot.command(description='Not for you to use')
async def reload(ctx, extension=None):
    await ctx.defer(ephemeral=True)
    if not await bot.is_owner(ctx.author):
        print(f"{ctx.author} tried to use the reload command")
        await ctx.respond('I told you in the description this is not for you to use, you Dingus!')
        return
    try:
        if extension is not None:
            bot.reload_extension(f'cogs.{extension}')
        else:
            for stuff in allCogs:
                bot.reload_extension(f'cogs.{stuff}')
        print("\n\n\n\n\n\n\n\n\n\nreloaded")
        await ctx.respond('Done', ephemeral=True)
    except discord.ExtensionError as e:
        await ctx.respond(f"Error: {str(e)}", ephemeral=True)    
    except Exception as e:
        await ctx.respond(f"Unexpected error: {str(e)}", ephemeral=True)

'''
@bot.command(description='Not for you to use')
async def reload(ctx, extension=None):
    await ctx.defer(ephemeral=True)
    if not await bot.is_owner(ctx.author):
        print(f"{ctx.author} tried to use the reload command")
        await ctx.respond('I told you in the description this is not for you to use, you Dingus!')
        return
    try:
        
        if extension is not None:
'''

@bot.command()
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")
    print("recived")

for stuff in allCogs:
    bot.load_extension(f'cogs.{stuff}')    

bot.run(discordToken)

