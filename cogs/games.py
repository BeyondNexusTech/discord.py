import random
from discord.ext import commands

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="roll", description="Joue avec le Bot au lancé de dé", brief="Lance un dé")
    async def roll(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(f'{ctx.author.name} lance un dé et obtient : {result}')

    @commands.hybrid_command(name="headsortails", description="Joue avec le Bot à Pile ou Face", brief="Pile ou Face ?", help_command="Je test mon helper")
    async def headsortails(self, ctx):
        result = random.choice(['pile', 'face'])
        await ctx.send(f'Résulat obtenu : {result}')

async def setup(bot):
  await bot.add_cog(GamesCog(bot))
