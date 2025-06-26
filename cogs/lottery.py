import discord
from discord.ext import commands

import json

class View(discord.ui.View):
    @discord.ui.button(label='dingus',style=discord.ButtonStyle.primary)
    async def button_callback(self,button,interaction):
        await interaction.response.send_message('dingus',ephemeral=True)


class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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