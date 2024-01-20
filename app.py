from telethon import TelegramClient, events
import telethon
import aiohttp
import textwrap
import os
import requests
import json
import random
from discord_webhook import DiscordWebhook



url = "discord webhook"
appid = "telegram app id" 
apihash = "telegram api hash" 
apiname = "telegram api name"
dlloc = "/home/ec2-user/telegramtodiscord/" # file adress app is stored
input_channels_entities = "channel id"
blacklist = False
translate = 0

if blacklist == 'True':
    blacklist = True
if input_channels_entities is not None:
  input_channels_entities = list(map(int, input_channels_entities.split(',')))


def start():
    client = TelegramClient(apiname, 
                            appid, 
                            apihash)
    client.start()
    print('Started')
    print(f'Input channels: {input_channels_entities}')
    print(f'Blacklist: {blacklist}')
    @client.on(events.NewMessage(chats=input_channels_entities, blacklist_chats=blacklist))
    async def handler(event):
        if (type(event.chat)==telethon.tl.types.User):
          return #Ignore Messages from Users or Bots
        msg = event.message.message

        if event.message.media is not None and event.message.file: # If message has media
            dur = event.message.file.duration # Get duration
            print(dur)
            if dur is None: # If duration is none
              dur=1 # Set duration to 1

            path = await event.message.download_media(dlloc)
            print(path,msg,event.chat.title)  
            discord_with_media(msg,path)
            os.remove(path)
        else: # No media text message
          discord_bot(msg)

        
    client.run_until_disconnected()


def discord_bot(text):
    mUrl = url

    data = {"content": text}
    requests.post(mUrl, json=data)

def discord_with_media(text,media):
  

  webhook = DiscordWebhook(url=url,  content=text) 

  # send two images
  with open(media, "rb") as f:
    filex = media.split("/")[-1]
    webhook.add_file(file=f.read(), filename=filex)

  response = webhook.execute()
    


if __name__ == "__main__":
    start()
