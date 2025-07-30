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
            await message.send("You can't count twice in a row, dingus!")
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
            try:
                print(eval(message.content))
            except Exception as e:
                return
        self.bot.file_manager.save_saves()

def setup(bot):
    bot.add_cog(Counting(bot))