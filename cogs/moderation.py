import discord
from discord.ext import commands

# Created the Moderation class which allows adding moderation commands
class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Added kick command if user has rights
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} was excluded.")
    
    # Command to add the specified role when adding the reaction on the rules message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            result = await self.reaction_checker(payload)
            if result:
                await result["member"].add_roles(result["role"])
                print(f"The role '{result["role"].name}' has been added to {result["member"].name}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Commands to remove the specified role when removing the reaction on the rules message
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            result = await self.reaction_checker(payload)
            if result:
                await result["member"].remove_roles(result["role"])
                print(f"The role '{result["role"].name}' has been deleted {result["member"].name}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Function to check and control that the reaction is correct and is assigned to the correct message
    async def reaction_checker(self, payload):
        if str(payload.message_id) == str(self.bot.DISCORD_RULES_MESSAGE_ID):
            if str(payload.emoji) == str(self.bot.DISCORD_EMOJI_REACTION):
                guild = self.bot.get_guild(payload.guild_id)
                if guild:
                    member = await guild.fetch_member(payload.user_id)
                    if member:
                        role = discord.utils.get(guild.roles, name="Membre")
                        if role:
                            result = { "member": member, "role": role }
                            return result
                        else:
                            raise ValueError(f"The role was not found: {role}")
                    else:
                        raise ValueError(f"The member was not found on the server: {member}")
                else:
                    raise ValueError(f"The server was not found: {guild}")
            else:
                raise ValueError(f"The reaction used is not the correct one: {payload.emoji}")
        else:
            raise ValueError(f"The message is not the right one: {payload.message_id}")
    
async def setup(bot):
  await bot.add_cog(ModerationCog(bot))
