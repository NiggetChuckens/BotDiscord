from dotenv import load_dotenv
from discord.ext import commands
import os, discord, asyncio, tempfile, sys
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

sys.path.append('src/modules')
sys.path.append('src/modules/jpaw')
sys.path.append('src/modules/himatimes')

load_dotenv()

##################################################################################
# Intents for the bot
intents = discord.Intents.all()
intents.guilds = True

bot = commands.Bot(command_prefix='^', intents=intents)
slash = SlashCommand(bot, sync_commands=True)



##################################################################################
# Bot events
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    await slash.sync_all_commands()


##################################################################################
#JPAW paste commands
@commands.has_role(889001453316878367)        
@slash.slash(name="Paste",
             description="Genera paste de emision",
             options=[
                 create_option(
                    name="status",
                    description="Finalizado o Emision",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="version_1",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="version_2",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=False
                ),
                create_option(
                    name="version_3",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=False
                ),
                create_option(
                    name="version_4",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=False
                ),
                create_option(
                    name="version_5",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=False
                ),
                create_option(
                    name="version_6",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=False
                )
             ])
async def paste(ctx: SlashContext, status, version_1 = '', version_2 = '', version_3 = '', version_4 = '', version_5 = '', version_6 = ''):
    """
    Handles the creation of multiple pastes and sends a response with the generated paste URL.
    Args:
        ctx (SlashContext): The context of the command.
        status (str): The status to be included in the paste.
        version_1 (str, optional): The first version to be included in the paste. Defaults to ''.
        version_2 (str, optional): The second version to be included in the paste. Defaults to ''.
        version_3 (str, optional): The third version to be included in the paste. Defaults to ''.
        version_4 (str, optional): The fourth version to be included in the paste. Defaults to ''.
        version_5 (str, optional): The fifth version to be included in the paste. Defaults to ''.
        version_6 (str, optional): The sixth version to be included in the paste. Defaults to ''.
    Returns:
        None
    """
    from jpawPaste import createPaste
    from database import new_paste

    if ctx.guild_id != 294403414442639360:
        await ctx.send("Este comando solo esta disponible en el servidor de Japan Paw")
        return
    
    await ctx.defer()
    
    response = '' 
    response2 = '' 
    response3 = '' 
    response4 = '' 
    response5 = ''  
    response6 = ''
    fansub = ''
    fansub2 = ''
    fansub3 = ''
    fansub4 = ''
    fansub5 = ''
    fansub6 = ''    
    
    if version_2 != '':
        name2, fansub2, response2 = await createPaste(status, version_2)
    if version_3 != '':
        name3, fansub3, response3 = await createPaste(status, version_3)
    if version_4 != '':
        name4, fansub4, response4 = await createPaste(status, version_4)
    if version_5 != '':
        name5, fansub5, response5 = await createPaste(status, version_5)
    if version_6 != '':
        name6, fansub6, response6 = await createPaste(status, version_6)

    name, fansub, response = await createPaste(status, version_1)

    paste_url = await new_paste(name, 
                                response, 
                                response2, 
                                response3, 
                                response4, 
                                response5, 
                                response6,
                                fansub,
                                fansub2,
                                fansub3,
                                fansub4,
                                fansub5,
                                fansub6)
    
    embed = discord.Embed(title="Paste Generado",
              description=f"El siguiente es el enlace de tu paste:\n\nhttps://paste.japan-paw.net/?v={paste_url}",
              color=discord.Color.green())

    await ctx.send(embed=embed)
    
    
@slash.slash(name="Buscar_paste",
              description="Busca paste por nombre",
              options=[
                  create_option(
                      name="anime",
                      description="Nombre del anime",
                      option_type=3,
                      required=True
                  )
              ])
async def Buscar_paste(ctx: SlashContext, anime):
    """
    Handles the Buscar_paste command to search for anime paste links in the database and send the results in chunks.
    Args:
        ctx (SlashContext): The context of the command.
        anime (str): The name of the anime to search for.
    Returns:
        None
    Behavior:
        - Checks if the command is used in the specific guild (server) with ID 294403414442639360.
        - If not, sends a message indicating the command is only available in the specified server.
        - Defers the response to allow for processing time.
        - Searches for the anime in the database.
        - Splits the search results into chunks of 25 items.
        - For each chunk, constructs a list of URLs truncated to fit within Discord's character limit.
        - Sends an embedded message with the search results.
    """
    from database import search_anime
    
    if ctx.guild_id != 294403414442639360:
        await ctx.send("Este comando solo esta disponible en el servidor de Japan Paw")
        return

    await ctx.defer()

    chunk_size = 25
    result = search_anime(anime)
    chunks = [result[i:i+chunk_size] for i in range(0, len(result), chunk_size)]

    for chunk in chunks:
        truncated_urls = []
        current_length = 0
        for item in chunk:
            if not truncated_urls or current_length + len(item[1]) <= 4091:
                truncated_urls.append(f'[{item[1]}](https://paste.japan-paw.net/?v={item[0]})')
                current_length += len(item[1]) + 5

        url = '\n'.join(truncated_urls)

        embed = discord.Embed(title=f"Paste encontrados con el nombre: {anime}",
                              description=f"{url}",
                              color=discord.Color.green())

        msg = await ctx.send(embed=embed)
        
# @commands.has_role(889001453316878367)
# @slash.slash(name="newCap",
#              description="Genera paste para nuevo capitulo en emision",
#              options=[
#                  create_option(
#                     name="number",
#                     description="Numero del capitulo",
#                     option_type=3,
#                     required=True
#                 ),
#                 create_option(
#                     name="routes",
#                     description="Rutas del capitulo",
#                     option_type=3,
#                     required=True
#                 ),
#              ])
# async def newCap(ctx: SlashContext, number, routes):
#     from jpawPaste import newemisionCap
#
#     if ctx.guild_id != 294403414442639360:
#         await ctx.send("Este comando solo esta disponible en el servidor de Japan Paw")
#         return
#     response = await newemisionCap(number, routes)    
#     embed = discord.Embed(title="Paste generado", 
#                         description=f"El paste ha sido generado correctamente\n\n```{response}```", 
#                         color=discord.Color.green()
#                         )
#     msg = await ctx.send(embed=embed)
#     await asyncio.sleep(15)
#     await msg.delete()
# 
# ##################################################################################
# #Moderation commands
# 
# @slash.slash(name="purge")
# async def purge(ctx: SlashContext, amount: int = 1):
#     from moderation import clear
#     await clear(ctx, amount)
    
    
##################################################################################
#Bot run
bot.run(os.getenv('JPAW'))