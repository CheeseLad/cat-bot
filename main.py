#!/usr/bin/env python3

import os
import random
import discord
with open('token.txt', 'r') as f:
    token = f.read()

cat_gifs = []
with open('cat-gifs.txt', 'r') as f:
    for line in f:
        cat_gifs.append(line.strip())

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        member_count = sum(1 for _ in client.get_all_members())
        guild_count = sum(1 for _ in client.guilds)
        client.activity = discord.Game(name=f'with {member_count} cats')
        print(f'Playing with {member_count} cats in {guild_count} guilds')
        print('------')
    async def on_message(self, message):
        
        if message.author.id == self.user.id:
            return

        if  message.content.startswith('!cat'):
            print(f"{message.author} used '!cat'")
            response = random.choice(cat_gifs)
            await message.reply(f'{response}', mention_author=True)

    

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(token)

