import discord
from discord.ext import commands, tasks
import datetime

import random

class DNE(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        

def setup(bot):
    bot.add_cog(DNE(bot))
