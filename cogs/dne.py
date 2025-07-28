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
        
    #TODO The timer doesn't work. Right now, the 15 minutes apply to all monsters, not just the one you are attacking.
    @discord.ui.button(label="Attack!", style=discord.ButtonStyle.red, custom_id="attack")
    async def attack(self, button, interaction):        
        #await interaction.response.defer()
        self.bot.file_manager.load_saves() #Makes sure the file is ready

        message = str(interaction.message.id)
        if message not in self.bot.file_manager.saves['dne']['monsters']: #Adds monster to the file if it is new
            
            self.bot.file_manager.saves['dne']['monsters'][message] = [random.randint(1200,1750),{}]
            self.bot.file_manager.save_saves() #Saves it. Save saves also reloads the file

        save = self.bot.file_manager.saves['dne']['monsters'][message]
        timestamp = int(time.time())
        member = str(interaction.user.id)
        attack = random.randint(150, 250)
        coupons = random.randint(100, 250)

        self.bot.file_manager.check_member(member)
        timer = save[1]

        if member not in timer or timer[member] <= timestamp:
            print('attacked',message,save)
            self.bot.file_manager.saves['dne']['monsters'][message][1][member] = timestamp + 900 #15 min
            self.bot.file_manager.saves['dne']['monsters'][message][0] -= attack
            self.bot.file_manager.saves['members'][member][0] += coupons
            await interaction.response.send_message(f'Glory be! <@{member}> smote the {self.monster} for {attack} HP, and gained {coupons} coupons!')

            if self.bot.file_manager.saves['dne']['monsters'][message][0] <= 0:
                self.bot.file_manager.saves['members'][member][0] += 500
                await interaction.followup.send(f'Huzzah! The {self.monster} has been vanquished by <@{member}>! For dealing the final blow, <@{member}> has earned an additional 500 coupons.')
                del self.bot.file_manager.saves['dne']['monsters'][message]
                await interaction.message.delete()
        else:
            await interaction.response.send_message(f"You're still on cooldown. Try again in <t:{timer[member]}:R>",ephemeral=True)
            print('failed')
        self.bot.file_manager.save_saves()
        return
    
class PVPView(discord.ui.View):
    def __init__(self, bot, target, coupons):
        self.bot = bot
        self.target = target
        self.coupons = coupons

        super().__init__(timeout=None)
    
    @discord.ui.button(label="Grab Coupons!", style=discord.ButtonStyle.green, custom_id="attack")
    async def take(self,button,interaction):
        self.bot.file_manager.check_member(str(interaction.user.id))
        self.bot.file_manager.check_member(str(self.target.id))

        self.bot.file_manager.saves['members'][str(self.target.id)][0] -= self.coupons
        self.bot.file_manager.saves['members'][str(interaction.user.id)][0] += self.coupons
        self.bot.file_manager.save_saves()

        await interaction.response.send_message(f'You have picked up {self.coupons} coupons!',ephemeral=True)

        button.disabled = True
        button.label = 'Someone already grabbed the coupons, you greedy ho!'
        await interaction.message.edit(view=self)

class DNE(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.monster.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View(self.bot,None))
        self.bot.add_view(PVPView(self.bot,None,None))  

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

    def pvp(self):
        def_rng = random.randint(1,20)
        atk_rng = random.randint(1,20)
        
        if def_rng == 20:
            return -1
        if atk_rng > def_rng:
            if atk_rng >= 18:
                return 2
            return 1
        return 0
    
    def check_channel(self,name):
        return 'battle-arena' in name.lower() or 'dne' in name.lower()

    @commands.slash_command(description='Rizz')
    async def rizz(self, ctx, target: discord.User):
        self.bot.file_manager.check_member(str(ctx.author.id))
        self.bot.file_manager.check_member(str(target.id))  

        if ctx.author.id == target.id:
            await ctx.respond("You can't rizz yourself, you dingus!")
            return

        if not self.check_channel(ctx.channel.name):
            await ctx.respond("Go to the battle arena channel, you nerd!")
            return
        
        rng = self.pvp()
        if rng == -1:
            message = f'<@{ctx.author.id}> tried to rizz <@{target.id}>, but <@{target.id}> rolled a nat 20 saving throw. Your words fall on deaf ears.'
            image = discord.File('./rizzfail.jpg', filename='image.png')
        elif rng == 0:
            message = f"<@{ctx.author.id}> tried to rizz <@{target.id}> but they aren't falling for those cheesy lines. You are shot down!"
            image = discord.File('./rizzfail.jpg', filename='image.png')
        elif rng == 1:
            message = f'<@{ctx.author.id}> rizzed <@{target.id}>. What a simp!'
            image = discord.File('./chad.jpg', filename='image.png')
        elif rng == 2:
            coupons = random.randint(100,500)
            message = f"<@{ctx.author.id}> rizzed <@{target.id}> and because they're such a simp they tossed {coupons} of their Hello Fresh coupons at your feet; quick pick it up!"
            image = discord.File('./chad.jpg', filename='image.png')
            view = PVPView(self.bot, target, coupons)
            embed = discord.Embed(
                title='Rizz!!!',
                description=message
            )
            embed.set_image(url='attachment://image.png')
            await ctx.respond(embed=embed, file=image, view=view)
            return

        embed = discord.Embed(
            title='Rizz!!!',
            description=message
        )
        embed.set_image(url='attachment://image.png')
        await ctx.respond(embed=embed, file=image)

    @commands.slash_command(description='Fireball')
    async def fireball(self, ctx, target: discord.User):
        self.bot.file_manager.check_member(str(ctx.author.id))
        self.bot.file_manager.check_member(str(target.id))

        if ctx.author.id == target.id:
            await ctx.respond("You can't fireball yourself, you dingus!")
            return

        if not self.check_channel(ctx.channel.name):
            await ctx.respond("Go to the battle arena channel, you nerd!")
            return

        rng = self.pvp()
        if rng == -1:
            message = f'<@{ctx.author.id}> tried to cast fireball at <@{target.id}>, but <@{target.id}> rolled a nat 20 saving throw. The fireball landed at their feet; you missed!'
            image = discord.File('./fireballfail.jpg', filename='image.png')
        elif rng == 0:
            message = f"<@{ctx.author.id}> tried to cast fireball at <@{target.id}> in a small area. It backfired. Burn!"
            image = discord.File('./fireballfail.jpg', filename='image.png')
        elif rng == 1:
            message = f'<@{ctx.author.id}> hit <@{target.id}> with a fireball. Good shot!'
            image = discord.File('./gandalf.jpg', filename='image.png')
        elif rng == 2:
            coupons = random.randint(100,500)
            message = f"<You fireballed <@{target.id}> and because you threw such an epic shot, they dropped {coupons} of their Hello Fresh coupons; quick pick it up!"
            image = discord.File('./gandalf.jpg', filename='image.png')
            view = PVPView(self.bot, target, coupons)
            embed = discord.Embed(
                title='Fireball Throw',
                description=message
            )
            embed.set_image(url='attachment://image.png')
            await ctx.respond(embed=embed, file=image, view=view)
            return

        embed = discord.Embed(
            title='Fireball Throw',
            description=message
        )
        embed.set_image(url='attachment://image.png')
        await ctx.respond(embed=embed, file=image)

    @commands.slash_command(description='Whack')
    async def whack(self, ctx, target: discord.User):
        self.bot.file_manager.check_member(str(ctx.author.id))
        self.bot.file_manager.check_member(str(target.id))

        if ctx.author.id == target.id:
            await ctx.respond("You can't whack yourself, you dingus!")
            return

        if not self.check_channel(ctx.channel.name):
            await ctx.respond("Go to the battle arena channel, you nerd!")
            return

        rng = self.pvp()
        if rng == -1:
            message = f'<@{ctx.author.id}> tried to whack <@{target.id}>, but <@{target.id}> rolled a nat 20 saving throw. Your attack misses completely!'
            image = discord.File('./whackfail.jpg', filename='image.png')
        elif rng == 0:
            message = f"<@{ctx.author.id}> tried to whack <@{target.id}> but failed miserably!"
            image = discord.File('./whackfail.jpg', filename='image.png')
        elif rng == 1:
            message = f'<@{ctx.author.id}> whacked <@{target.id}>. Ouch!'
            image = discord.File('./knight.jpg', filename='image.png')
        elif rng == 2:
            coupons = random.randint(100,500)
            message = f"<@{ctx.author.id}> whacked <@{target.id}> swith a sword and because you dealt such an epic blow, they dropped {coupons} of their Hello Fresh coupons; quick pick it up!"
            image = discord.File('./knight.jpg', filename='image.png')
            view = PVPView(self.bot, target, coupons)
            embed = discord.Embed(
                title='Whack!',
                description=message
            )
            embed.set_image(url='attachment://image.png')
            await ctx.respond(embed=embed, file=image, view=view)
            return

        embed = discord.Embed(
            title='Whack!',
            description=message
        )
        embed.set_image(url='attachment://image.png')
        await ctx.respond(embed=embed, file=image)
def setup(bot):
    bot.add_cog(DNE(bot))
