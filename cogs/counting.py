import discord
from discord.ext import commands
import requests
import random

class Counting(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        
        if 'counting' not in message.channel.name:
            return
        
        print(self.bot.file_manager.saves.setdefault('counting', [0, None]))
        
        if message.author.id == self.bot.file_manager.saves['counting'][1]:
            await message.channel.send("You can't count twice in a row, dingus!")
            self.bot.file_manager.saves['counting'] = [0, None]

        if message.content.isdigit():
            number = int(message.content)
            if number == self.bot.file_manager.saves['counting'][0] + 1:
                self.bot.file_manager.saves['counting'] = [number,message.author.id]  
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"Wrong number! The next number should be {self.bot.file_manager.saves['counting'][0] + 1}.")
                self.bot.file_manager.saves['counting'] = [0, None]
        else:
            response = requests.get("httpsd://api.mathjs.org/v4/", params={"expr": message.content})
            if response.status_code != 200:
                return
            if not response.text.isdigit():
                return 
            number = int(response.text)
            if number == self.bot.file_manager.saves['counting'][0] + 1:
                self.bot.file_manager.saves['counting'] = [number,message.author.id]  
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"Wrong number! The next number should be {self.bot.file_manager.saves['counting'][0] + 1}.")
                self.bot.file_manager.saves['counting'] = [0, None]
            
        self.bot.file_manager.save_saves()

def setup(bot):
    bot.add_cog(Counting(bot))