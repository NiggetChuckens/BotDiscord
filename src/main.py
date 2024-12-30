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
#@commands.has_role(889001453316878367)        
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
    from jpawPaste import createPaste
    from database import new_paste

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
    print(fansub, name)

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
    
    url = f'https://paste.japan-paw.net/?v={paste_url}'
    embed = discord.Embed(title="Paste Generado",
              description=f"El siguiente es el enlace de tu paste:\n\n{url}",
              color=discord.Color.green())

    await ctx.send(embed=embed)
    
        
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
bot.run(os.getenv('YUKITEST'))