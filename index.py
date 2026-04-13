"""
Discord Bot - Archiel Bot
A Discord bot that responds to specific messages from a target user with greeting and latency check functionalities.
Environment Variables Required:
    - TOKEN: Discord bot token for authentication
    - TARGET_USER_ID: User ID of the target user to respond to
    - MY_USER_ID: User ID of the bot owner for testing commands
Features:
    - Responds to greeting messages ('Hai', 'hai', 'Hi', 'hi') from target user
    - Provides latency check via 'ping'/'Ping'/'PING' commands (owner only)
    - Implements message cooldown to prevent spam (6-second delay between responses)
    - Logs all bot activities and received/sent messages
⚠️ DISCORD TERMS OF SERVICE (ToS) COMPLIANCE NOTES:
    - Ensure this bot complies with Discord's ToS (https://discord.com/terms)
    - Do NOT use this bot for:
        * Spam, harassment, or automated abuse
        * Violating user privacy or collecting personal data without consent
        * Circumventing Discord's security measures
        * Scraping or unauthorized data collection
    - Implement proper rate limiting to avoid API abuse
    - Respect user consent and obtain necessary permissions
    - Do not impersonate other users or services
    - Ensure the bot has appropriate intents configured in Discord Developer Portal
    - The 6-second cooldown is implemented to prevent excessive message flooding
Global Variables:
    - is_request_to_sent_message: Flag to prevent concurrent message sending during cooldown
Events:
    - on_ready(): Triggered when bot successfully connects to Discord
    - on_message(): Triggered when a message is received in any channel the bot can access
"""

from dotenv import load_dotenv
from logger import logger
import discord
import time
import os
load_dotenv()

# Ambil token dan target user ID dari environment variables
TOKEN = os.getenv('TOKEN').strip()
TARGET_USER_ID = int(os.getenv('TARGET_USER_ID'))
MY_USER_ID = int(os.getenv('MY_USER_ID'))
client = discord.Client()

# Variable Local.
is_request_to_sent_message = False


@client.event
async def on_ready():
    # Log saat bot berhasil login
    # logger("[BOT STATUS]:", f"{client.user} has logged in successfully.")
    await client.change_presence(
        status=discord.Status.dnd,
    )
    # print(f'Hi {client.user}, Please say hi to Archiel')
    logger("[BOT STATUS]:", "Bot is ready and waiting for messages.")
    logger("[TIP]:", "Please say hi to Archiel")

@client.event
async def on_message(message):
    global is_request_to_sent_message

    # Log pesan yang diterima
    logger(
        "[MESSAGE RECEIVED]:",
        f'Message received from "{message.author.name}"' +
        f' ({message.author.display_name})' if message.author.display_name != message.author.name else '',
        f'with content "{message.content}"' if message.content else 'with no content',
        f'in server "{message.guild.name}"' if message.guild else 'in Direct Message',
        f'and ID "{message.author.id}"'
    )

    # Menghindari pengiriman pesan berulang jika sudah ada permintaan untuk mengirim pesan
    if is_request_to_sent_message == True:
        return
    
    # Test my bot.
    cek_latency_commands = ['ping', 'Ping', 'PING']
    if message.author.id == MY_USER_ID and message.content in cek_latency_commands:
        is_request_to_sent_message = True
        await message.channel.send(f"**Pong!** My latency is {round(client.latency * 1000)}ms ({client.latency:.2f}s)\n**Note:** This is a test message for latency check.")
        logger(
            "[MESSAGE SENT]:",
            "[OWNER]:",
            f'Message has been sent to "{message.author.name}" with ID "{message.author.id}"'
        )
        time.sleep(6)  # Tambahkan delay sebelum mengizinkan pengiriman pesan berikutnya (opsional) => 6 detik
        is_request_to_sent_message = False
        return

    # Cek apakah pesan berasal dari bot itu sendiri atau bukan dari target user ID
    if message.author.id == client.user.id:
        return
    if message.author.id != TARGET_USER_ID:
        return

    # Message yang diterima dari user dengan ID TARGET_USER_ID
    # [-- Message Filtering --]
    listSayhi = ['Hai', 'hai', 'Hi', 'hi']  # List kata-kata yang akan memicu balasan

    # if message.content.startswith(tuple(listSayhi)):    # Cek apakah pesan dimulai dengan salah satu kata dalam listSayhi
    if message.content in listSayhi:    # Beside <string>.startswith('Hai') or use a tuple like ('Hai', 'hai', 'Hi', 'hi') for startswith.
        # Kirim balasan ke channel yang sama
        is_request_to_sent_message = True
        time.sleep(6)  # Tambahkan delay sebelum mengirim balasan (opsional) => 6 detik
        await message.channel.send(f"Hai juga <@{TARGET_USER_ID}>")
        # Log pesan yang dikirim
        logger(
            "[MESSAGE SENT]:",
            "[TARGET USER]:",
            f'Message has been sent to "{message.author.name}" with ID "{message.author.id}"'
        )
        is_request_to_sent_message = False
        return


# Jalankan bot dengan token yang diambil dari environment variables
client.run(TOKEN)