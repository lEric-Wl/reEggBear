import discord
from discord.ext import commands, tasks
import datetime

import json
import random

class View(discord.ui.View):
    def __init__(self,bot):
        super().__init__(timeout=None)  # Set timeout to None so the view is permanent
        self.bot=bot
        for i in [1,5,10]:
            self.add_item(self.make_buttons(i))

    def buy_ticket(self, memberId, amount):
        self.bot.file_manager.check_member(memberId)
        saves = self.bot.file_manager.saves

        if memberId not in saves['lottery']:
            saves['lottery'][memberId] = 0
        
        if saves['members'][memberId][0] < amount * 100:
            return False
        
        saves['lottery'][memberId] += amount
        saves['lottery']['total'] += amount
        saves['members'][memberId][0] -= amount * 100
        self.bot.file_manager.save_saves()

        return True
        
    def make_buttons(self,amount):
        button = discord.ui.Button(
                label=f"{amount} ticket{'s' if amount > 1 else ''}",
                style=discord.ButtonStyle.green,
                custom_id=f"{amount}ticket{'s' if amount > 1 else ''}"
        )    
        
        async def callback(interaction):
            member = str(interaction.user.id)
            buy = self.buy_ticket(member, amount)
            if not buy:
                await interaction.respond("You don't have enough coupons", ephemeral=True)
            else: 
                await interaction.respond(f"You successfully bought {amount} ticket{'s' if amount > 1 else ''}", ephemeral=True)

        button.callback = callback
        return button

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_winner.start()

        self.saves_file = 'saves.json'
        self.saves = None
        self.load_saves()

        self.message = None

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

            Each ticket costs 100 coupons. Winners will be selected every day at 18:00 UTC +0.
            
            The current jackpot is **1100 coupons!**
            '''
            )

        embed.set_thumbnail(url='attachment://image.jpeg')

        self.message = await ctx.respond(embed=embed,file=thumbnail,view=View(self.bot))

    @tasks.loop(time=datetime.time(hour=18,minute=0, tzinfo=datetime.timezone.utc))
    async def get_winner(self):
        channel = self.bot.get_channel(1380610958350618786)
        image = discord.File('./lotteryWinner.gif',filename='image.gif')

        self.bot.file_manager.load_saves()

        lottery = self.bot.file_manager.saves['lottery']
        totalTickets = lottery['total']

        if totalTickets == 0:
            image = discord.File('./noWinner.jpg',filename='image.gif')        
            embed = discord.Embed(
                title = "Lottery Results",
                description = "No one bought a ticket for today's lottery drawing, so no one won. Boo!"
            )
            embed.set_thumbnail(url='attachment://image.gif')
            await channel.send(embed=embed,file=image)
            return
        
        rng = random.randint(1,totalTickets)
        prize = 1000 + 100*totalTickets
        winner = '0'
        image = discord.File('./lotteryWinner.gif',filename='image.gif')

        for stuff,thing in lottery.items():
            if stuff == 'total':
                continue

            rng -= thing
            if rng <= 0:
                winner = stuff
                self.check_member(winner)
                self.bot.file_manager.saves['members'][winner][0] += prize
                
                lottery = {'total': 0}  # Reset the lottery
                self.bot.file_manager.save_saves()
                break


        embed = discord.Embed(
            title = "Lottery Results",
            description = f"Congratulations! {(await self.bot.fetch_user(int(winner))).mention} just won {prize} coupons!"
        )
        embed.set_image(url='attachment://image.gif')

        await channel.send(embed=embed,file=image)            
        

def setup(bot):
    bot.add_cog(Lottery(bot))