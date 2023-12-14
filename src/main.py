import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import mysql.connector

load_dotenv()
bot = commands.Bot(command_prefix='^', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')    

@bot.command(aliases=["purge", "delete"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 1):
    await ctx.channel.purge(limit=amount + 1)

@bot.command(name="jumbo")
async def jumbo(ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)

positions = {key: (f'<:{name}:{id}>', name.replace('_', ' ').title()) for key, (name, id) in {
    'tr': ('Traduccion', '1059298060112507021'),
    'cc': ('Correccion', '1059298054622171207'),
    'ti': ('Tiempos', '1059298058573205545'),
    'ed': ('Edicion', '1059298055951749281'),
    'fx': ('Efectos', '1059308406181199963'),
    'ec': ('Encode', '1059298057201651722'),
    'qc': ('Control_Calidad', '1059298053095444570'),
}.items()}

async def update_status_in_db(database, name, n_epi, prev_done):
    cursor = database.cursor()
    query = "UPDATE status SET listo = %s WHERE alias = %s AND episodio = %s"
    cursor.execute(query, (prev_done, name, n_epi))
    database.commit()
    cursor.close()

async def send_status_embed(ctx, name, n_epi, action, status_emoji, prev_done, image_url):
    embed = DiscordEmbed(title=f'• {name}.', color=int('7997191'))
    embed.add_embed_field(name=f'‣ Episodio {n_epi}: {action} {status_emoji}', value=f'{prev_done}', inline=False)
    embed.set_thumbnail(url=image_url)
    hook = os.getenv('STATUS_HOOK')
    webhook = DiscordWebhook(hook, username='Estado de proyectos - UnsyncSubs', avatar_url='https://cdn.discordapp.com/attachments/1032453549940035587/1036097508423782431/p_003_1.jpg')
    webhook.add_embed(embed)
    response = webhook.execute()
    webhook.remove_embeds()

async def add_show_to_db(database, titulo, alias, episodio, listo, imagen):
    cursor = database.cursor()
    query = "INSERT INTO status (titulo, alias, episodio, listo, imagen) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (titulo, alias, episodio, listo, imagen))
    database.commit()
    cursor.close()
    

@bot.command()
@commands.has_role('Staff')
async def status(ctx, name: str, n_epi: int = None, to_do: str = None, position: str = None):
    position = position.lower()
    if position not in positions:
        await ctx.send(f"Posición inválida. Las posiciones válidas son: {list(positions.keys())}")
        return
    emoji, action = positions[position]
    status_emoji = '<a:Listo:1151660812759478342>' if to_do.lower() == 'done' else '<a:NoListo:1180891701200568390>'
    with mysql.connector.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME')
    ) as database:
        try:    
            cursor = database.cursor()
            query = "SELECT * FROM status WHERE alias = %s AND episodio = %s"
            cursor.execute(query, (name, n_epi))
            rows = cursor.fetchall()
            found_episode = False
            for row in rows:
                if row[1] == name and row[2] == n_epi:
                    found_episode = True
                    prev_done = f'{row[3]} {emoji} ' if to_do.lower() == 'done' else row[3].replace(f'{emoji} ', '')
                    await update_status_in_db(database, name, n_epi, prev_done)
                    await send_status_embed(ctx, row[0], n_epi, action, status_emoji, prev_done, row[4])                
            if not found_episode: 

                query = "SELECT titulo, alias, imagen FROM status WHERE alias = %s LIMIT 1"
                cursor.execute(query, (name,))
                result = cursor.fetchall()

                for row in result:
                    show = row[0]
                    alias = row[1]
                    imagen = row[2]
                await ctx.send(f"{show} no tiene el episodio {n_epi} en la base de datos, se agregará ahora.")
                await add_show_to_db(database, titulo=show, alias=alias, episodio=n_epi, listo=emoji, imagen=imagen)
                await ctx.send(f"El capitulo {n_epi} del anime {name} ha sido agregado a la base de datos.")
                await send_status_embed(ctx, show, n_epi, action, '<a:Listo:1151660812759478342>', emoji, imagen)

        except Exception :
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
            name, alias, episodio, imagen, listo = name.content, alias.content, episodio.content, imagen.content, listo.content
            emoji, action = positions[listo.lower()]
            await add_show_to_db(database, titulo=name, alias=alias, episodio=episodio, listo=emoji, imagen=imagen)
            await send_status_embed(ctx, name, episodio, action, '<a:Listo:1151660812759478342>', emoji, imagen)
            await ctx.send(f"El capitulo {n_epi} del anime {name} ha sido agregado a la base de datos.")
        
        
 
 
           
bot.run(os.getenv('DISCORD_TOKEN'))
