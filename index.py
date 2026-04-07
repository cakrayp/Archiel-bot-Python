import discord
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv('TOKEN')
TARGET_USER_ID = int(os.getenv('TARGET_USER_ID'))
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.dnd,
    )
    print(f'Hi {client.user}, please say hi to Archiel')

@client.event
async def on_message(message):
   if message.author.id == client.user.id:
        return
   if message.author.id != TARGET_USER_ID:
        return

   if message.content.startswith('Hai'):
        await message.channel.send(f"Hai juga <@{TARGET_USER_ID}>")

client.run(TOKEN)
