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
            self.saves['members'][memberId] = 0
            self.save_saves()

    def check_member(self, memberId):
        if(self.bot.get_user(int(memberId)).bot):
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
        self.saves['members'][member] += random.randint(5, 20) 
        self.save_saves()

    @discord.slash_command()
    async def check_balance(self, ctx):         
        member = ctx.author.id
        self.check_member(member)
        balance = self.saves['members'][member]

        embed = discord.Embed(
            title=f'Currency Balances for {ctx.author.name}',
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(name=f'**Holding:** {balance} Hello Fresh Coupons',value='')

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
    