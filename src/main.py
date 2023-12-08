import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import mysql.connector

load_dotenv()
bot = commands.Bot(command_prefix='^', intents=discord.Intents.all())
#tree = discord.app_commands.CommandTree(discord.Client(intents=discord.Intents.all()))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')    

@bot.command(aliases= ["purge","delete"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    try:
        if amount is None:
            await ctx.channel.purge(limit=2)
        else:
            amount = int(amount)+1
            await ctx.channel.purge(limit=amount)
    except Exception:
        await ctx.send("No tienes permisos para usar este comando.")
        
@bot.command(name="jumbo")
async def jumbo(ctx, emoji: discord.Emoji):
    try:
        await ctx.send(emoji.url)
    except Exception:
        await ctx.send("Error: Emoji no encontrado en la lista de servidores.")

positions={'tr':('<:Traduccion:1059298060112507021>', 'Traducción'), 
               'cc':('<:Correccion:1059298054622171207>', 'Corrección'), 
               'ti':('<:Tiempos:1059298058573205545>', 'Tiempos'), 
               'ed':('<:Edicion:1059298055951749281>', 'Edición'), 
               'fx':('<:Efectos:1059308406181199963>', 'Efectos'), 
               'ec':('<:Encode:1059298057201651722>', 'Encode'), 
               'qc':('<:Encode:1059298057201651722>', 'QC')}

@bot.command()
@commands.has_role('Staff')
async def status(ctx, name: str, n_epi: int = None, to_do: str = None, position: str = None):
    position = position.lower()
    if position not in positions.keys():
        await ctx.send(f"Posición inválida. Las posiciones válidas son: {positions.keys()}")
    with mysql.connector.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME')
    ) as database:
        cursor = database.cursor()
        emoji, action = positions[position]
        query = "SELECT * FROM status WHERE alias = %s AND episodio = %s"
        cursor.execute(query, (name, n_epi))
        rows = cursor.fetchall()        
        prev_done = ''
        if to_do.lower() == 'done':
            status_emoji = '<a:Listo:1151660812759478342>'
        elif to_do.lower() == 'undone':
            status_emoji = '<a:NoListo:1180891701200568390>'
        else:
            raise ValueError("Invalid to_do value")
        found_episode = False
        for row in rows:
            if row[1] == name:
                if row[2] == n_epi:
                    found_episode = True                                   
                titulo = f'• {row[0]}.'
                if to_do.lower() == 'done':
                    prev_done = f'{row[3]} {emoji} '
                elif to_do.lower() == 'undone':
                    prev_done = row[3].replace(f'{emoji} ', '')
                query = "UPDATE status SET listo = %s WHERE alias = %s"
                cursor.execute(query, (prev_done, name))
                database.commit()
                embed = DiscordEmbed(title=titulo, color=int('7997191'))
                embed.add_embed_field(name='‣ Episodio {}: {} {}'.format(n_epi, action, status_emoji), value='{}'.format(prev_done), inline=False)
                embed.set_thumbnail(url='https://cdn.myanimelist.net/images/anime/1943/127762l.jpg')
                hook = os.getenv('DISCORD_HOOK')
                webhook = DiscordWebhook(hook, username='Estado de proyectos - UnsyncSubs', avatar_url='https://cdn.discordapp.com/attachments/1032453549940035587/1036097508423782431/p_003_1.jpg')
                webhook.add_embed(embed)
                response = webhook.execute()
                webhook.remove_embeds()
                cursor.close()
        if not found_episode:
            await ctx.send(f"El capitulo {n_epi} del anime {name} no existe en la base de datos, contacta con un administrador para que lo agregue.")

bot.run(os.getenv('DISCORD_TOKEN'))