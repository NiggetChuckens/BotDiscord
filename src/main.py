import os
import json
import discord
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()
bot = commands.Bot(command_prefix='^', intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(discord.Client(intents=discord.Intents.all()))
token = os.getenv('DISCORD_TOKEN')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')    

@bot.command(aliases= ["purge","delete"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    try:
        if amount == None:
            await ctx.channel.purge(limit=2)
        else:
            amount = int(amount)+1
            await ctx.channel.purge(limit=amount)
    except:
        await ctx.send("You don't have the permission to do that!")

@bot.command()
async def jumbo(ctx, emoji: discord.Emoji = None):
    if emoji is not None:
        await ctx.send(str(emoji.url))
    else:
        await ctx.send("You didn't provide an emoji!")
        
        
        
        
@tree.command()
@commands.has_role('Staff')
async def status(ctx):
    with open(Path('BotDiscord/src/embeds/kimizero5.json'), 'r') as f:
        data = json.load(f)
    embed = DiscordEmbed.from_dict(data)
    webhook = 'https://discord.com/api/webhooks/1178251404188581949/aXJn9PoxTh4bXyrwSHs60nIIuV1W0woOovLrR4FQwMvEdx6WL27buEKiCRzkOwT4sm3N'
    webhook.add_embed(embed)
    response=webhook.execute()
bot.run(token)
