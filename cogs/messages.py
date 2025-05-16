import discord
import typing
from discord.ext import commands
from datetime import datetime

# Created the Message class which allows adding message commands
class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Function to send a message with the stream image in your Discord twitch chan
    async def send_stream_message(self, stream_datas) -> str | None:
        channel = self.bot.get_channel(int(self.bot.DISCORD_TWITCH_CHANNEL_ID))
        if channel:
            # Check if a message has already been sent for this stream
            if int(self.bot.TWITCH_LAST_MESSAGE_ID) == 0:
                try:
                    last_message = await channel.fetch_message(int(self.bot.TWITCH_LAST_MESSAGE_ID))
                    if last_message:
                        print("Message already sent for this stream.")
                        return
                except discord.NotFound:
                    print("Previous message not found, sending new message.")

                # If no previous message was found, or if the message was deleted, a new message is sent
                embed = discord.Embed(title=stream_datas["title"], color=discord.Color.green(), url="https://twitch.tv/YourStreamerName") \
                    .set_author(name="YourStreamerName", url="https://twitch.tv/YourStreamerName") \
                    .set_thumbnail(url="https://static-cdn.jtvnw.net/jtv_user_pictures/your_streamer_picture.png") \
                    .set_image(url=stream_datas["image_url"]) \
                    .add_field(name="Viewers", value=stream_datas["viewer_count"]) \
                    .set_footer(text="Twitch", icon_url="https://images-ext-1.discordapp.net/external/SL3ulKgL0oX0ytenjoilO7r6gXMNZfdwh7R1u__GGm4/https/cdn-longterm.mee6.xyz/plugins/twitch/logo.png")
                embed.timestamp = datetime.now()
                # Mention a role (replaces 'ROLE_ID' with the actual ID of the role)
                mention = self.bot.DISCORD_MEMBER_ROLE

                # Sends the message and saves the message ID
                sent_message = await channel.send(content=f"{mention}, I'm live on Twitch !\n https://twitch.tv/YourStreamerName !", embed=embed)
                self.bot.TWITCH_LAST_MESSAGE_ID = sent_message.id
                print(f"Message sent with ID: {self.bot.TWITCH_LAST_MESSAGE_ID}")

        else:
            print(f"Error : Unable to find Discord channel with ID {channel}.")    
    
    @commands.hybrid_command(name="send_embed_message", description="Send an embed message by choosing the channel", brief="Sending an embed")
    @commands.has_role("Administrator")
    async def send_embed_message(self, ctx, channel: str,
        title: str, description: str, color: typing.Optional[str] = "blue", url: typing.Optional[str] = None,
        author_name: typing.Optional[str] = None, author_url: typing.Optional[str] = "", author_icon: typing.Optional[str] = "",
        url_thumbnail: typing.Optional[str] = None, url_image: typing.Optional[str] = None,
        footer_text: typing.Optional[str] = None, footer_icon: typing.Optional[str] = "", footer_timestamp: typing.Optional[bool] = False,
        fields: typing.Optional[str] = None, reaction: typing.Optional[str] = None) -> str | None:

        # Checking all form filling dependencies
        if author_url and not author_name:
            return await ctx.send("```asciidoc\nThe author name must be entered if you enter the author URL :: \n```")
        if author_icon and not author_name:
            return await ctx.send("```asciidoc\nThe author name must be entered if you enter the author icon :: \n```")
        
        if author_url and not author_url.startswith("https://"):
            return await ctx.send("```diff\n- The URL of the author received is not compliant\n```")
        if author_icon and not author_icon.startswith("https://"):
            return await ctx.send("```diff\n- The URL of the icon received is not compliant```")
        
        if url_thumbnail and not url_thumbnail.startswith("https://"):
            return await ctx.send("```diff\n- The URL of the thumbnail image received is not compliant```")
        
        if url_image and not url_image.startswith("https://"):
            return await ctx.send("```diff\n- The URL of the image received is not compliant```")
        
        if footer_icon and not footer_text:
             return await ctx.send("```asciidoc\nThe footer text must be filled in if you fill in the footer icon :: \n```")
        # End of checks
        
        channel = self.bot.get_channel(int(channel))
        get_color = lambda name: getattr(discord.Color, name.lower(), lambda: discord.Color.default())()
        hex_color = get_color(color)
        
        if channel:
            if url and not url.startswith("https://"):
                return await ctx.send("```diff\n- The URL received is not compliant```")
            
            embed = discord.Embed(title=title, description=description, url=url, color=hex_color)

            # Implementation of the embed data to be sent
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
                return await ctx.send("```diff\n- The number of fields entered exceeds the maximum capacity: (25)```")
            
            if fields_list:
                for field in fields_list:
                    # Check and verify that the field name is correctly entered
                    name_param = field.split("\",")[0].strip()
                    if name_param.split("=")[0] == "name":
                        name_param = name_param.replace("name=", "")[1:]
                    else:
                        return await ctx.send(f"```diff\n- The name parameter of the '{name_param}' field has not been filled in```")

                    # Check and verify that the field value is correctly entered
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
                        return await ctx.send(f"```diff\n- The value parameter of the '{name_param}' field has not been filled in```")

                    # Inline parameter implementation if it is integrated into the fields or set to False by default
                    if len(field.split("\",")) > 2:
                        inline_param = field.split("\",")[2].strip()
                        if inline_param.split("=")[0] == "inline":
                            inline_param = inline_param.replace("inline=", "").replace(";", "")[1:]
                            if inline_param not in ["True", "true", "1", "False", "false", "0"]:
                                return await ctx.send(f"```diff\n- The inline parameter of the '{name_param}' field is not filled in correctly ('True', 'False')```")
                        else:
                            return await ctx.send(f"```diff\n- The inline parameter for field '{name_param}' has not been specified```")
                    else:
                        inline_param = "False"
                    
                    embed.add_field(name=f"{name_param}", value=f"{value_param}", inline=f"{inline_param}")
            # End of implementation
            
            sent_message = await channel.send(embed=embed)

            # Add reaction if specified for message
            if reaction:
                await sent_message.add_reaction(reaction)
            
            await ctx.send(f"```diff\n+ The message was successfully sent to the {channel.name} channel by the user {sent_message.author.name}```")
        else:
            return await ctx.send("```diff\n- The chan you wanted to send the message to was not found.```")

async def setup(bot):
    await bot.add_cog(MessageCog(bot))
