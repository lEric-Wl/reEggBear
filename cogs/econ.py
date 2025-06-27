import discord

import json

class Economy:
    def __init__(self, bot):
        self.bot = bot
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

    @discord.on_member_join()
    async def on_member_join(self,member):
        memberId = member.id
        if memberId not in self.saves['members']:
            self.add_member(memberId)
            
def setup(bot):
    bot.add_cog(Economy(bot))
    