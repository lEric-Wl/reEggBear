import discord
from discord.ext import commands

import json

class View(discord.ui.View):
    def __init__(self,bot):
        super().__init__(timeout=None)  # Set timeout to None so the view is permanent
        self.saves_file = 'saves.json'
        self.saves = None
        self.load_saves()
        self.bot=bot

    def load_saves(self):
        with open(self.saves_file, 'r') as saves:
            self.saves = json.load(saves)
            saves.close()

    def save_saves(self):
        with open(self.saves_file, 'w') as saves:
            json.dump(self.saves, saves, indent=4)
        self.load_saves()

    def add_member(self, memberId):
        if memberId not in self.saves['members']:
            self.saves['members'][memberId] = [0,0] #Holding, Bank
            self.save_saves()

    def check_member(self, memberId):
        self.load_saves()
        user = self.bot.get_user(int(memberId))
        if user is None or user.bot:
            return 
        
        if memberId not in self.saves['members']:
            self.add_member(memberId)

    def buy_ticket(self, memberId, amount):
        self.load_saves()
        self.check_member(memberId)
        if memberId not in self.saves['lottery']:
            self.saves['lottery'][memberId] = 0
        
        if self.saves['members'][memberId][0] < amount * 100:
            return False
        self.saves['lottery'][memberId] += amount
        self.saves['members'][memberId][0] -= amount * 100
        self.save_saves()

        return True
        

    @discord.ui.button(label='1 ticket',style=discord.ButtonStyle.primary, custom_id='1ticket')
    async def callback1(self,button,interaction):
        member = str(interaction.user.id)
        buy = self.buy_ticket(member,1)
        if not buy:
           await interaction.respond("You don't have enough coupons",ephemeral=True)
        else: 
            await interaction.respond("You successfully bought 1 ticket",ephemeral=True)

    @discord.ui.button(label='5 tickets',style=discord.ButtonStyle.primary, custom_id='5tickets')
    async def callback5(self,button,interaction):
        member = str(interaction.user.id)
        buy = self.buy_ticket(member,5)
        if not buy:
           await interaction.respond("You don't have enough coupons",ephemeral=True)
        else: 
            await interaction.respond("You successfully bought 5 ticket",ephemeral=True)

    @discord.ui.button(label='10 tickets',style=discord.ButtonStyle.primary, custom_id='10tickets')
    async def callback10(self,button,interaction):
        member = str(interaction.user.id)
        buy = self.buy_ticket(member,10)
        if not buy:
           await interaction.respond("You don't have enough coupons",ephemeral=True)
        else: 
            await interaction.respond("You successfully bought 10 ticket",ephemeral=True)

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View(self.bot))

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

        await ctx.respond(embed=embed,file=thumbnail,view=View(self.bot))


def setup(bot):
    bot.add_cog(Lottery(bot))