from dotenv import load_dotenv
from discord.ext import commands
import sys, os, mysql.connector, discord

# Add himatimes folder to the path so we can import stuff needed
sys.path.append('src/modules/himatimes')
from embed_stuff import status as anime_status, add_show_to_db, positions
from db_actions import check_db_info, send_status_embed

# We define the bot and the intents
intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix='^', intents=intents)

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
    
async def dbinfo(ctx):
    await check_db_info(ctx, table=f'{ctx.guild.name.lower()}_anime')