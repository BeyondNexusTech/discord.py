import os
import discord
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class YourBot(commands.Bot):
    async def setup_hook(self):
        # Environment variable for Discord
        self.DISCORD_GUILD_ID               = os.getenv("DISCORD_GUILD_ID")
        self.DISCORD_TWITCH_CHANNEL_ID      = os.getenv("DISCORD_TWITCH_CHANNEL_ID")
        self.DISCORD_RULES_CHANNEL_ID       = os.getenv("DISCORD_RULES_CHANNEL_ID")
        self.DISCORD_RULES_MESSAGE_ID       = os.getenv("DISCORD_RULES_MESSAGE_ID")
        self.DISCORD_MEMBER_ROLE            = os.getenv("DISCORD_MEMBER_ROLE")
        self.DISCORD_EMOJI_REACTION         = os.getenv("DISCORD_EMOJI_REACTION")
        
        # Environment variable for Twitch
        self.TWITCH_CLIENT_ID               = os.getenv("TWITCH_CLIENT_ID")
        self.TWITCH_CLIENT_SECRET           = os.getenv("TWITCH_CLIENT_SECRET")
        self.TWITCH_OAUTH_TOKEN             = os.getenv("TWITCH_OAUTH_TOKEN")
        self.TWITCH_LAST_MESSAGE_ID         = os.getenv("TWITCH_LAST_MESSAGE_ID")

        # Loader for all extensions you have create
        for extension in ["games", "moderation", "messages", "twitch"]:
            await self.load_extension(f"cogs.{extension}")

intents = discord.Intents.all()
bot = YourBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

    # Synced all commands created for the bot and uploaded them to discord (Ctrl + R for reload Discord App)
    synced = await bot.tree.sync()
    print(f"{len(synced)} commands synced to the the servers!")
    
    twitch_cog = bot.cogs["TwitchCog"]
    message_cog = bot.cogs["MessageCog"]
    
    # Retrieves an access token via the Client Credentials Flow
    access_token = twitch_cog.get_access_token()
    
    if access_token:
        # Checks if the streamer named in the bot is online
        is_online, stream_datas = twitch_cog.is_streaming(access_token)

        # Send a message with the saved image if he is online
        if is_online and stream_datas:
            await message_cog.send_stream_message(stream_datas)

    # Configure the bot to check the stream status every 5 minutes
    while True:
        if access_token:
            is_online, stream_datas = twitch_cog.is_streaming(access_token)
            if is_online and stream_datas:
                await message_cog.send_stream_message(stream_datas)
            else:
                # If the stream is offline, reset last_message_id
                bot.TWITCH_LAST_MESSAGE_ID = int(0)
                print("Stream offline, counter reset.")
        await asyncio.sleep(300)

bot.run(token=DISCORD_TOKEN)
