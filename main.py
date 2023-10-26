#!/usr/bin/env python3

import os
import random
import discord
import requests
import json
from config import discord_token as token, tenor_token as tenor, forbidden;
import logging
import logging.handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,
    backupCount=5,
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

BASE_URL = 'https://api.tenor.com/v1/'
ENDPOINT = 'random'
params = {
    'key': tenor,
    'q': 'cat',
    'limit': 1  
}

chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0","1","2","3","4","5","6","7","8","9"]

def tenor_cat():
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    print(response)
    if response.status_code == 200:
      data = response.json()
      gif_url = data['results'][0]['media'][0]['gif']['url']
      print("Random Cat GIF URL:", gif_url)
      return gif_url
    else:
      print(f"Error: {response.status_code}")
      return None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('---------------------------------------------')
        member_count = sum(1 for _ in client.get_all_members())
        guild_count = sum(1 for _ in client.guilds)
        await client.change_presence(activity=discord.Game(name=f'with {member_count} cats in {guild_count} homes (!cat, !add [link], !random)'))
        print(f'Playing with {member_count} cats in {guild_count} homes (!cat, !add [link], !random)')
        print('------------------')
    async def on_message(self, message):
        
        if message.author.id == self.user.id:
            return
        
        if  message.content.startswith('!help'):
            print(f"{message.author} used '!help'")
            await message.reply("Commands:\n\n`!add` - Adds an image\n`!cat`", mention_author=True)

        """if message.content.startswith('!remove'):
            response = message.content[5:]
            with open('cat-gifs.txt', 'w') as f:
                if response in f.readlines():
                    await message.reply(f'Removed <{response}> successfully', mention_author=True)
                    f.write(response + '\n')"""

        if  message.content.startswith('!cat'):
            print(f"{message.author} used '!cat'")
            cat_gifs = []
            with open('cat-gifs.txt', 'r') as f:
                for line in f:
                  cat_gifs.append(line.strip())
            response = random.choice(cat_gifs)
            await message.reply(f'{response}', mention_author=True)

        if  message.content.startswith('!add'):
            print(f"{message.author} used '!add'")
            response = message.content[5:]
            with open('cat-gifs.txt', 'r') as f:
                curr_list = []
                for item in f.readlines():
                    curr_list.append(item.strip())
                
                if response in curr_list and "http" in response and response in forbidden:
                        await message.reply(f'Already added that GIF', mention_author=True)
                else:
                    with open('cat-gifs.txt', 'a') as f:
                      f.write(response + '\n')
                      await message.reply(f'Added GIF successfully.', mention_author=True)
                      

        if  message.content.startswith('!random'):
            print(f"{message.author} used '!random'")
            link = "https://prnt.sc/"
            for i in range(0, 6):
              link += chars[random.randint(0, len(chars) - 1)]
            await message.reply(f'{link}', mention_author=True)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(token, log_handler=None)

