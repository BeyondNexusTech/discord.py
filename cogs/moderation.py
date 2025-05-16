import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} a été exclu(e).")
    
    # Fonction pour vérifier et contrôler que le message et l'emoji sont bien ceux choisis
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
                            raise ValueError(f"Le rôle n'a pas été trouvé: {role}")
                    else:
                        raise ValueError(f"Le membre n'a pas été trouvé sur le serveur: {member}")
                else:
                    raise ValueError(f"Le serveur n'a pas été trouvé: {guild}")
            else:
                raise ValueError(f"La réaction utilisée n'est pas la bonne: {payload.emoji}")
        else:
            raise ValueError(f"Le message n'est pas le bon : {payload.message_id}")
    
    # Commande pour ajouter le rôle spécifié lors de l'ajout de la réaction sur le message des regles
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            result = await self.reaction_checker(payload)
            if result:
                await result["member"].add_roles(result["role"])
                print(f"Le rôle '{result["role"].name}' a été ajouté à {result["member"].name}")
        except Exception as e:
            print(f"Erreur: {e}")
    
    # Commandes pour supprimer le rôle spécifié lors de la suppression de la réaction sur le message des regles
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            result = await self.reaction_checker(payload)
            if result:
                await result["member"].remove_roles(result["role"])
                print(f"Le rôle '{result["role"].name}' a été supprimé à {result["member"].name}")
        except Exception as e:
            print(f"Erreur: {e}")
    
async def setup(bot):
  await bot.add_cog(ModerationCog(bot))