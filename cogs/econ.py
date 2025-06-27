import discord
from discord.ext import commands

import json
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saves_file = 'saves.json'
        self.saves = None
        self.load_saves()

    def load_saves(self):
        with open(self.saves_file, 'r') as saves:
            self.saves = json.load(saves)

    def save_saves(self):
        with open(self.saves_file, 'w') as saves:
            json.dump(self.saves, saves, indent=4)

    def add_member(self, memberId):
        if memberId not in self.saves['members']:
            self.saves['members'][memberId] = [0,0] #Holding, Bank
            self.save_saves()

    def check_member(self, memberId):
        user = self.bot.get_user(int(memberId))
        if user is None or user.bot:
            return 
        
        if memberId not in self.saves['members']:
            self.add_member(memberId)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.check_member(str(member.id))
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        member = str(message.author.id)

        self.check_member(member)
        self.saves['members'][member][0] += random.randint(5, 20) 
        self.save_saves()

    def getBalance(self, memberId):
        self.check_member(memberId)
        balance = self.saves['members'][memberId]

        return balance

    @commands.slash_command()
    async def check_balance(self, ctx):  
        print('received')       
        member = ctx.author.id
        
        balance = self.getBalance(str(member))

        embed = discord.Embed(
            title=f'Currency Balances for {ctx.author.name}',
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(name=f'**Holding:** {balance[0]} Hello Fresh Coupons',value='')

        await ctx.respond(embed=embed)

    @discord.slash_command()
    async def deposit(self,ctx,amount:int):
        member = str(ctx.author.id)

        if amount > self.getBalance(member)[0]:
            await ctx.respond("You don't have that much, dingus")

        self.getBalance(member)[1] += amount
        self.getBalance(member)[0] -= amount

        embed  = discord.Embed(
            title=f"You've successfully deposited {amount} Hello Fresh Coupons into your bank!"
        )

        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(Economy(bot))
    