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
        #await interaction.response.defer()
        self.bot.file_manager.load_saves() #Makes sure the file is ready
        message = str(interaction.message.id)
        if message not in self.bot.file_manager.saves['dne']['monsters']: #Adds monster to the file if it is new
            self.bot.file_manager.saves['dne']['monsters'][message] = random.randint(1200,1750) 
            self.bot.file_manager.save_saves() #Saves it. Save saves also reloads the file

        timestamp = int(time.time())
        member = str(interaction.user.id)
        attack = random.randint(150, 250)
        coupons = random.randint(100, 250)

        self.bot.file_manager.check_member(member)
        timer = self.bot.file_manager.saves['timer']['dne']

        if member not in timer or timer[member] <= timestamp:
            print('attacked')
            self.bot.file_manager.saves['timer']['dne'][member] = timestamp + 900 #15 min
            self.bot.file_manager.saves['dne']['monsters'][message] -= attack
            self.bot.file_manager.saves['members'][member][0] += coupons
            await interaction.response.send_message(f'Glory be! <@{member}> smote the {self.monster} for {attack} HP, and gained {coupons} coupons!')

            if self.bot.file_manager.saves['dne']['monsters'][message] <= 0:
                self.bot.file_manager.saves['members'][member][0] += 500
                await interaction.followup.send(f'Huzzah! The {self.monster} has been vanquished by <@{member}>! For dealing the final blow, <@{member}> has earned an additional 500 coupons.')
                del self.bot.file_manager.saves['dne']['monsters'][message]
                await interaction.message.delete()
        else:
            await interaction.response.send_message(f"You're still on cooldown. Try again in <t:{self.bot.file_manager.saves['timer']['dne'][member]}:R>",ephemeral=True)
            print('failed')
        self.bot.file_manager.save_saves()
        return
    
    
class DNE(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.monster.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View(self.bot,None))

    @tasks.loop(time=[
        datetime.time(hour=5, minute=0, tzinfo=datetime.timezone.utc),
        datetime.time(hour=13, minute=0, tzinfo=datetime.timezone.utc),
        datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc)
    ])
    async def monster(self):
        channel = self.bot.get_channel(1397568088622235750)
        await channel.send(f'<@&1387579469749030934> warriors! A new foe approaches. Band together to defeat it!')

        monster = random.choice(['mike'])
        image = discord.File(f'{monster}.png', filename='image.png')

        embed = discord.Embed(
            title = f'Defeat the {monster}!',
            description='Whach this monster to make him drop coupons from his hoard.'
        )
        embed.set_image(url='attachment://image.png')
        await channel.send(embed=embed, file=image, view=View(self.bot,monster))
        return

    @commands.slash_command(description='Rizz')
    async def rizz(self,ctx,target):
        atk_rng = random.randint(1,20)
        def_rng = random.randint(1,20)

        if def_rng == 20:
            message = f'<@{ctx.author.id}> tried to rizz <@{target.id}>, but <@{target.id}> rolled a nat 20 saving throw. Your words fall on deaf ears.'
            image = discord.File('./rizzfail.jpg', filename='image.png')
        elif atk_rng > def_rng:
            message = f'<@{ctx.author.id}> rizzed <@{target.id}>. What a simp!'
            image = discord.File('./chad.jpg', filename='image.png')
        else:
            message = f"<@{ctx.author.id}> tried to rizz <@{target.id}> but they aren't falling for those cheesy lines. You are shot down!"
            image = discord.File('./rizzfail.jpg', filename='image.png')

        embed = discord.Embed(
            title='Rizz!!!',
            description=message
        )
        embed.set_image(url='attachment://image.png')

        await ctx.respond(embed=embed, file=image)

def setup(bot):
    bot.add_cog(DNE(bot))
