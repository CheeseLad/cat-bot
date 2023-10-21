#!/usr/bin/env python3

import os
import random
import discord

cat_gifs = []
for files in os.listdir("./cat-gifs"):
    cat_gifs.append(files)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        member_count = sum(1 for _ in client.get_all_members())
        guild_count = sum(1 for _ in client.guilds)
        client.activity = discord.Game(name=f'with {member_count} cats')
        print(f'Playing with {member_count} cats in {guild_count} guilds')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if  message.content.startswith('!cat'):
            response = random.choice(cat_gifs)
            await message.reply(file=discord.File(f'./cat-gifs/{response}'), mention_author=True)

    

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run('MTE2NTMyNzc3NTcwODc0OTkxNQ.GrYHzY.2z2mMzhkxH63kMZxW4rASdTFo61Mxi8ZrLvG_w')

