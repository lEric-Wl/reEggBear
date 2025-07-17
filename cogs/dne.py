import discord
from discord.ext import commands, tasks
import datetime

import random

class View(discord.ui.View):
    def __init__(self,bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.health = random.randint(1200, 1750)
        self.attack = random.randint(150, 250)
        self.coupons = random.randint(100, 250)

    @discord.ui.button(label="Attack!", style=discord.ButtonStyle.red, custom_id="attack")
    async def attack(self, button, interaction):


        member = str(interaction.user.id)

        
        await interaction.message.delete()
    
    

class DNE(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @tasks.loop(time=[
        datetime.time(hour=5, minute=0, tzinfo=datetime.timezone.utc),
        datetime.time(hour=13, minute=0, tzinfo=datetime.timezone.utc),
        datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc)
    ])
    async def temp(self):
        return 
    
    @discord.slash_command()
    async def monster(self,ctx):
        await ctx.respond(f'<@&1387579469749030934> warriors! A new foe approaches. Band together to defeat it!')

        monster = random.choice(['mike'])
        image = discord.File(f'{monster}.png', filename='image.png')

        embed = discord.Embed(
            title = f'Defeat the {monster}!',
            description='Whach this monster to make him drop coupons from his hoard.'
        )
        embed.set_image(url='attachment://image.png')
        await ctx.send(embed=embed, file=image, view=View(self.bot))
        return

def setup(bot):
    bot.add_cog(DNE(bot))
