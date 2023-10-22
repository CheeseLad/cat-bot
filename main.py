#!/usr/bin/env python3

import os
import random
import discord
import requests
import json

with open('keys.txt', 'r') as f:
    keys = f.read().splitlines()
    token = keys[0]
    tenor = keys[1]

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

        if  message.content.startswith('!cat'):
            print(f"{message.author} used '!cat'")
            cat_gifs = []
            with open('cat-gifs.txt', 'r') as f:
                for line in f:
                  cat_gifs.append(line.strip())
            response = random.choice(cat_gifs)
            #tenor_cat()
            await message.reply(f'{response}', mention_author=True)

        if  message.content.startswith('!add'):
            print(f"{message.author} used '!add'")
            response = message.content[5:]
            with open('cat-gifs.txt', 'a') as f:
                f.write(response + '\n')
            await message.reply(f'Added <{response}> successfully', mention_author=True)

        if  message.content.startswith('!ping'):
            print(f"{message.author} used '!ping'")
            times = int(message.content[6])
            user_to_ping = message.content[8:]
            
            for i in range(0, times):
                await message.reply(f'{user_to_ping}', mention_author=False)

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
client.run(token)
