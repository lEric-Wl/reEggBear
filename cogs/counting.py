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
        
        count = self.bot.file_manager.saves['counting'][0]
        prev = self.bot.file_manager.saves['counting'][1]
        if message.author.id == prev:
            await message.channel.send(f"<@{message.author.id}> ruined it at **{count}**. You can't count twice in a row!\n\nThe next number is **1**")
            await message.add_reaction('❌')
            self.bot.file_manager.saves['counting'] = [0, None]
            self.bot.file_manager.save_saves()
            return

        if message.content.isdigit():
            number = int(message.content)
            if number == count + 1:
                self.bot.file_manager.saves['counting'] = [number,message.author.id]  
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"<@{message.author.id}> ruined it at **{count}**. Wrong number!\n\nThe next number is **1**")
                self.bot.file_manager.saves['counting'] = [0, None]
        else:
            response = requests.get("https://api.mathjs.org/v4/", params={"expr": message.content.lower()})
            if response.status_code != 200:
                return
            if not response.text.isdigit():
                return 
            number = int(response.text)
            if number == count + 1:
                self.bot.file_manager.saves['counting'] = [number,message.author.id]  
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"<@{message.author.id}> ruined it at **{count}**. Wrong number!\n\nThe next number is **1**")
                self.bot.file_manager.saves['counting'] = [0, None]
            
        self.bot.file_manager.save_saves()

async def setup(bot):
    bot.add_cog(Counting(bot))