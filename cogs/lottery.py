import discord
from discord.ext import commands, tasks
import datetime

import random

class View(discord.ui.View):
    def __init__(self,bot):
        super().__init__(timeout=None)  # Set timeout to None so the view is permanent
        self.bot=bot

        for i in [1,5,10]:
            self.add_item(self.make_buttons(i))
    
    async def buy_ticket(self,  memberId, amount):
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
            thumbnail = discord.File('./gamblingMeme.jpeg',filename='image.jpeg')

            buy = await self.buy_ticket(member, amount)
            if not buy:
                await interaction.respond("You don't have enough coupons", ephemeral=True)
            else: 
                await interaction.respond(f"You successfully bought {amount} ticket{'s' if amount > 1 else ''}", ephemeral=True)
                embed=discord.Embed(
                    title='Egg Bear Lottery!',
                    description=f'''Enter to win some Hello Fresh coupons!

                    Each ticket costs 100 coupons. Winners will be selected every day at 18:00 UTC +0.
                    
                    The current jackpot is **{1000 + 100 * self.bot.file_manager.saves['lottery']['total']} coupons!**
                    '''
                )
                embed.set_thumbnail(url='attachment://image.jpeg')
                await interaction.message.edit(embed=embed, file = thumbnail, attachments=[], view=View(self.bot))    

        button.callback = callback
        return button

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_winner.start()

        self.message = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View(self.bot))

    @commands.slash_command(description="Enter the lottery!")
    async def lottery(self, ctx):
        thumbnail = discord.File('./gamblingMeme.jpeg',filename='image.jpeg')
    
        embed = discord.Embed(
            title='Egg Bear Lottery!',
            description=f'''Enter to win some Hello Fresh coupons!

Each ticket costs 100 coupons. Winners will be selected every day at 18:00 UTC +0.
                
The current jackpot is **{1000 + 100 * self.bot.file_manager.saves['lottery']['total']} coupons!**
            '''
            )

        embed.set_thumbnail(url='attachment://image.jpeg')

        await ctx.respond(embed=embed,file=thumbnail,view=View(self.bot))

    @tasks.loop(time=datetime.time(hour=18,minute=00, tzinfo=datetime.timezone.utc))
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
                self.bot.file_manager.check_member(winner)
                self.bot.file_manager.saves['members'][winner][0] += prize
                
                self.bot.file_manager.saves['lottery'] = {'total': 0}
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