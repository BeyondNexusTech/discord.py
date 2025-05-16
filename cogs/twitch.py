import discord
import requests
from discord.ext import commands

# Creation of the Twitch class which allows the retrieval of the token and the verification of the streamer's status
class TwitchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Function for recovering the Twitch token if the streamer is live
    def get_access_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.bot.TWITCH_CLIENT_ID,
            "client_secret": self.bot.TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"Access Token: {access_token}")
            return access_token
        else:
            print(f"Error : {response.status_code} - {response.text}")
            return None
            
    # Check if the stream is online
    def is_streaming(self, access_token):
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": self.bot.TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {access_token}"
        }
        params = {
            "user_login": "YourStreamerName"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            # If the stream is live, we process the data to be returned
            if data["data"]:
                response = requests.get(data["data"][0]["thumbnail_url"].replace("{width}", "1280").replace("{height}", "720"))

                # Saving the Twitch thumbnail image so it is visible on Discord
                file_url = f"./stream_thumbnail/stream_{data['data'][0]['started_at']}.jpg"
                with open(file_url, "wb") as file:
                    file.write(response.content)
                    data["data"][0]["image_url"] = f"https://www.your_discord_bot_website.fr/stream_thumbnail/stream_{data['data'][0]['started_at']}.jpg"
                
                stream_datas = data['data'][0]
                return True, stream_datas
            else:
                print("The stream is offline.")
                return False, None
        else:
            print(f"Error : {response.status_code} - {response.text}")
            return False, None

async def setup(bot):
    await bot.add_cog(TwitchCog(bot))
