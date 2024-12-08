import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='^', intents=intents)

# Replace with your channel IDs
SOURCE_CHANNEL_ID = 1309971680415715369
TARGET_CHANNEL_ID = 987654321098765432

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id == SOURCE_CHANNEL_ID:
        if target_channel := bot.get_channel(TARGET_CHANNEL_ID):
            await target_channel.send(f'Update from {message.channel.name}: {message.content}')
    await bot.process_commands(message)
