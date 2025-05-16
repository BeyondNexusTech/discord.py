import random
from discord.ext import commands

# Creation of the Game class which allows the addition of mini-game commands
class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Added dice game command
    @commands.hybrid_command(name="roll", description="Play with the Bot at dice rolling", brief="Roll of dice", help_command="Use this command to roll a virtual die. The bot will tell you which number was rolled.")
    async def roll(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(f'{ctx.author.name} rolls a die and gets : **{result}**')

    # Added the Heads or Tails game command
    @commands.hybrid_command(name="headsortails", description="Play Heads or Tails with the Bot", brief="Heads or Tails?", help_command="Use this command to flip a virtual coin. The bot will tell you if it's heads or tails.")
    async def headsortails(self, ctx):
        result = random.choice(['head', 'tail'])
        await ctx.send(f'🪙 Result obtained : **{result}**')

async def setup(bot):
  await bot.add_cog(GamesCog(bot))
