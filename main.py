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


cat_gifs = []
with open('cat-gifs.txt', 'r') as f:
    for line in f:
        cat_gifs.append(line.strip())

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('---------------------------------------------')
        member_count = sum(1 for _ in client.get_all_members())
        guild_count = sum(1 for _ in client.guilds)
        await client.change_presence(activity=discord.Game(name=f'with {member_count} cats in {guild_count} homes'))
        print(f'Playing with {member_count} cats in {guild_count} guilds')
        print('------------------')
    async def on_message(self, message):
        
        if message.author.id == self.user.id:
            return

        if  message.content.startswith('!cat'):
            print(f"{message.author} used '!cat'")
            response = random.choice(cat_gifs)
            tenor_cat()
            await message.reply(f'{response}', mention_author=True)

    

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(token)
