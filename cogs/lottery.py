import discord
from discord.ext import commands

import json

class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Set timeout to None so the view is permanent

    @discord.ui.button(label='1 ticket',style=discord.ButtonStyle.primary, custom_id='1ticket')
    async def callback1(self,button,interaction):
        await interaction.response.send_message('dingus',ephemeral=True)

    @discord.ui.button(label='5 tickets',style=discord.ButtonStyle.primary, custom_id='5tickets')
    async def callback5(self,button,interaction):
        await interaction.response.send_message('dingus',ephemeral=True)

    @discord.ui.button(label='10 tickets',style=discord.ButtonStyle.primary, custom_id='10tickets')
    async def callback10(self,button,interaction):
        await interaction.response.send_message('dingus',ephemeral=True)

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View())

    @commands.slash_command(description="Enter the lottery!")
    async def lottery(self, ctx):
        thumbnail = discord.File('./gamblingMeme.jpeg',filename='image.jpeg')

        embed = discord.Embed(
            title='Egg Bear Lottery!',
            description=f'''
            Enter to win some Hello Fresh coupons!

            Each ticket costs 100 coupons. Winners will be selected every day at 20:00 UTC +0.
            
            The current jackpot is **1100 coupons!**
            '''
            )

        embed.set_thumbnail(url='attachment://image.jpeg')

        await ctx.respond(embed=embed,file=thumbnail,view=View())


def setup(bot):
    bot.add_cog(Lottery(bot))