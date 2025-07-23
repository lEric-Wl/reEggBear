import discord
from discord.ext import commands, tasks
import datetime
import time

import random
    
class View(discord.ui.View):
    def __init__(self,bot,monster):
        super().__init__(timeout=None)
        self.bot = bot
        self.monster = monster
        

    @discord.ui.button(label="Attack!", style=discord.ButtonStyle.red, custom_id="attack")
    async def attack(self, button, interaction):
        self.bot.file_manager.load_saves()
    
        message = str(interaction.message.id)
        saves = self.bot.file_manager.saves
    
        monsters = saves.setdefault('dne', {}).setdefault('monsters', {})
        if message not in monsters:
            monsters[message] = random.randint(1200, 1750)
            self.bot.file_manager.save_saves()
    
        timestamp = int(time.time())
        member = str(interaction.user.id)
        attack = random.randint(150, 250)
        coupon = random.randint(100, 250)
    
        self.bot.file_manager.check_member(member)
    
        timer = saves.setdefault('timer', {}).setdefault('dne', {})
    
        if timer.get(member, 0) <= timestamp:
            print('attacked')
            timer[member] = timestamp + 900  # 15 min cooldown
            monsters[message] -= attack
            saves['members'][member][0] += coupon
            self.bot.file_manager.save_saves()
    
            await interaction.response.send_message(
                f'Glory be! <@{member}> smote the {self.monster} for {attack} HP, and gained {coupon} coupons!'
            )
    
            if monsters[message] <= 0:
                saves['members'][member][0] += 500
                await interaction.followup.send(
                    f'Huzzah! The {self.monster} has been vanquished by <@{member}>! '
                    f'For dealing the final blow, <@{member}> has earned an additional 500 coupons.'
                )
                del monsters[message]
                await interaction.message.delete()
                self.bot.file_manager.save_saves()
        else:
            cooldown = timer[member]
            await interaction.response.send_message(
                f"You're still on cooldown. Try again in <t:{cooldown}:R>", ephemeral=True
            )
            print('failed')
        return
    
class DNE(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View(self.bot,None))

    @tasks.loop(time=[
        datetime.time(hour=5, minute=0, tzinfo=datetime.timezone.utc),
        datetime.time(hour=13, minute=0, tzinfo=datetime.timezone.utc),
        datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc)
    ])
    async def monster(self,ctx):
        await ctx.respond(f'<@&1387579469749030934> warriors! A new foe approaches. Band together to defeat it!')

        monster = random.choice(['mike'])
        image = discord.File(f'{monster}.png', filename='image.png')

        embed = discord.Embed(
            title = f'Defeat the {monster}!',
            description='Whach this monster to make him drop coupons from his hoard.'
        )
        embed.set_image(url='attachment://image.png')
        await ctx.send(embed=embed, file=image, view=View(self.bot,monster))
        return

def setup(bot):
    bot.add_cog(DNE(bot))
