import os
import discord
import mysql.connector
from dotenv import load_dotenv
from discord.ext import commands
from modules.moderation import clear
from modules.db_actions import save_server_id_to_db, create_table_w_server_name, check_db_info, update_status_in_db, send_status_embed, add_show_to_db
from modules.embed_stuff import status as anime_status, positions

load_dotenv()
intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix='^', intents=intents)

@bot.event
async def on_guild_join(guild):
    server_name = guild.name
    with mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME')
        ) as db:
        await create_table_w_server_name(db, server_name)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')  
        
@bot.command(aliases=["purge", "delete", 'clear'])
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, amount: int = 1):
    await clear(ctx, amount)
@bot.command(name="jumbo")
async def jumbo(ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)
@bot.command(alias=['status', 'estado'])
@commands.has_role('Staff')
async def status(ctx, 
                name: str, 
                n_epi: int = None, 
                to_do: str = None, 
                position: str = None,
                ):
    result = await anime_status(ctx, name, n_epi, to_do, position, f'{ctx.guild.name.lower()}_anime')
    if result == False:
        database = mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME')
        )
        emoji, action = positions[position]
        await ctx.send("Ingrese el nombre del show")
        name=await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send("Ingrese el alias del show")
        alias=await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send("Ingrese el episodio")
        episodio=await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send("Ingrese el link de la imagen")
        imagen=await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send("Ingrese el estado del episodio")
        listo=await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send("Ingrese el link del webhook a usar")
        webhook=await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        name, alias, episodio, imagen, listo, webhook = name.content, alias.content, episodio.content, imagen.content, listo.content, webhook.content
        emoji, action = positions[listo.lower()]
        await add_show_to_db(database, table=f'{ctx.guild.name}_anime', titulo=name, alias=alias, episodio=episodio, listo=emoji, imagen=imagen, webhook=webhook)
        await send_status_embed(ctx, name, episodio, action, '<a:Listo:1151660812759478342>', emoji, imagen, webhook)
        await ctx.send(f"El capitulo {n_epi} del anime {name} ha sido agregado a la base de datos.")
    
@bot.command()
async def dbinfo(ctx):
    await check_db_info(ctx, table=f'{ctx.guild.name.lower()}_anime')
    
bot.run(os.getenv('DISCORD_TOKEN'))