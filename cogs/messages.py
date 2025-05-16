import discord
import typing
from discord.ext import commands
from datetime import datetime

class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Fonction pour envoyer un message avec l'image du stream dans Discord
    async def send_stream_message(self, stream_datas) -> str | None:
        channel = self.bot.get_channel(int(self.bot.DISCORD_TWITCH_CHANNEL_ID))
        if channel:
            # Vérifier si un message a déjà été envoyé pour ce stream
            if int(self.bot.TWITCH_LAST_MESSAGE_ID) == 0:
                try:
                    last_message = await channel.fetch_message(int(self.bot.TWITCH_LAST_MESSAGE_ID))
                    if last_message:
                        print("Message déjà envoyé pour ce stream.")
                        return
                except discord.NotFound:
                    print("Message précédent non trouvé, envoi d'un nouveau message.")

                # Si aucun message précédent n'a été trouvé, ou si le message a été supprimé, on envoie un nouveau message
                embed = discord.Embed(title=stream_datas["title"], color=discord.Color.green(), url="https://twitch.tv/Neshkel") \
                    .set_author(name="Neshkel", url="https://twitch.tv/Neshkel") \
                    .set_thumbnail(url="https://static-cdn.jtvnw.net/jtv_user_pictures/38c9040c-cf6f-4a57-9e19-1079043da340-profile_image-70x70.png") \
                    .set_image(url=stream_datas["image_url"]) \
                    .add_field(name="Viewers", value=stream_datas["viewer_count"]) \
                    .set_footer(text="Twitch", icon_url="https://images-ext-1.discordapp.net/external/SL3ulKgL0oX0ytenjoilO7r6gXMNZfdwh7R1u__GGm4/https/cdn-longterm.mee6.xyz/plugins/twitch/logo.png")
                embed.timestamp = datetime.now()
                # Mentionner un rôle (remplace 'ROLE_ID' par l'ID réel du rôle)
                mention = self.bot.DISCORD_MEMBER_ROLE

                # Envoie le message et enregistre l'ID du message
                sent_message = await channel.send(content=f"{mention}, Je suis en live sur Twitch !\n https://twitch.tv/Neshkel !", embed=embed)
                self.bot.TWITCH_LAST_MESSAGE_ID = sent_message.id
                print(f"Message envoyé avec ID: {self.bot.TWITCH_LAST_MESSAGE_ID}")

        else:
            print("Erreur : Impossible de trouver le canal Discord.")    
    
    @commands.hybrid_command(name="send_embed_message", description="Envoyer un message embed en choisissant le channel", brief="Envoi d'un embed")
    @commands.has_role("Administrateur")
    #async def send_embed_message(self, field: None):
    async def send_embed_message(self, ctx, channel: str,
    title: str, description: str, color: typing.Optional[str] = "blue", url: typing.Optional[str] = None,
    author_name: typing.Optional[str] = None, author_url: typing.Optional[str] = "", author_icon: typing.Optional[str] = "",
    url_thumbnail: typing.Optional[str] = None, url_image: typing.Optional[str] = None,
    footer_text: typing.Optional[str] = None, footer_icon: typing.Optional[str] = "", footer_timestamp: typing.Optional[bool] = False,
    fields: typing.Optional[str] = None, reaction: typing.Optional[str] = None) -> str | None:
        
        if author_url and not author_name:
            return await ctx.send("```asciidoc\nLe nom d'auteur doit être renseigné si vous renseignez l'URL de l'auteur :: \n```")
        if author_icon and not author_name:
            return await ctx.send("```asciidoc\nLe nom d'auteur doit être renseigné si vous renseignez l'icône de l'auteur :: \n```")
        
        if author_url and not author_url.startswith("https://"):
            return await ctx.send("```diff\n- L'URL de l'auteur reçu n'est pas conforme\n```")
        if author_icon and not author_icon.startswith("https://"):
            return await ctx.send("```diff\n- L'URL de l'icône reçu n'est pas conforme```")
        
        if url_thumbnail and not url_thumbnail.startswith("https://"):
            return await ctx.send("```diff\n- L'URL de l'image thumbnail reçu n'est pas conforme```")
        
        if url_image and not url_image.startswith("https://"):
            return await ctx.send("```diff\n- L'URL de l'image reçu n'est pas conforme```")
        
        if footer_icon and not footer_text:
             return await ctx.send("```asciidoc\nLe texte du pied de page doit être renseigné si vous renseignez l'icône de celui-ci :: \n```")
        
        channel = self.bot.get_channel(int(channel))
        get_color = lambda name: getattr(discord.Color, name.lower(), lambda: discord.Color.default())()
        hex_color = get_color(color)
        
        if channel:
            if url and not url.startswith("https://"):
                return await ctx.send("```diff\n- L'URL reçu n'est pas conforme```")
            
            embed = discord.Embed(title=title, description=description, url=url, color=hex_color)
            
            if author_name:
                embed.set_author(name=f"{author_name}", url=f"{author_url}", icon_url=f"{author_icon}")
            
            if url_thumbnail:
                embed.set_thumbnail(url=f"{url_thumbnail}")
            
            if url_image:
                embed.set_image(url=f"{url_image}")
            
            if footer_text:
                embed.set_footer(text=f"{footer_text}", icon_url=f"{footer_icon}")
            
            if footer_timestamp:
                embed.timestamp = datetime.now()
            
            if fields:
                fields_list = fields.split("; ")
            else:
                fields_list = None
            
            if fields_list and len(fields_list) > 25:
                return await ctx.send("```diff\n- Le nombre de champ renseigné dépasse la capacité maximum (25)```")
            
            if fields_list:
                for field in fields_list:
                    name_param = field.split("\",")[0].strip()
                    if name_param.split("=")[0] == "name":
                        name_param = name_param.replace("name=", "")[1:]
                    else:
                        return await ctx.send(f"```diff\n- Le paramètre name du champ '{name_param}' n'a pas été renseigné```")
                    
                    value_param = field.split("\",")[1].strip()
                    if value_param.split("=")[0] == "value":
                        value_param = value_param.replace("value=", "")
                        if value_param.find("- "):
                            values_list = value_param.split("*  ")
                            for key, value in enumerate(values_list):
                                values_list[key] = value.replace("\"", "")
                            
                            value_param = "\n".join(values_list)
                        else:
                            value_param = value_param[1:]
                    else:
                        return await ctx.send(f"```diff\n- Le paramètre value du champ '{name_param}' n'a pas été renseigné```")
                    
                    if len(field.split("\",")) > 2:
                        inline_param = field.split("\",")[2].strip()
                        if inline_param.split("=")[0] == "inline":
                            inline_param = inline_param.replace("inline=", "").replace(";", "")[1:]
                            if inline_param not in ["True", "true", "1", "False", "false", "0"]:
                                return await ctx.send(f"```diff\n- Le paramètre inline du champ '{name_param}' n'est pas renseigné comme il faut ('True', 'False')```")
                        else:
                            return await ctx.send(f"```diff\n- Le paramètre inline du champ '{name_param}' n'a pas été renseigné```")
                    else:
                        inline_param = "False"
                    
                    embed.add_field(name=f"{name_param}", value=f"{value_param}", inline=f"{inline_param}")
            
            sent_message = await channel.send(embed=embed)
            if reaction:
                await sent_message.add_reaction(reaction)
            
            await ctx.send(f"```diff\n+ Le message à bien été envoyé sur la salon {channel.name} par l'utilisateur {sent_message.author.name}```")
        else:
            return await ctx.send("```diff\n- Le salon sur lequel envoyé le message n'a pas été trouvé```")

async def setup(bot):
    await bot.add_cog(MessageCog(bot))