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
                    name="routes",
                    description="Rutas de los capitulos",
                    option_type=3,
                    required=True
                ),
             ])
async def paste(ctx: SlashContext, status, routes):
    from jpawPaste import createPaste
    name, fansub, response = await createPaste(status, routes)
    print(fansub, name)
    fansub = fansub.replace(name, "")
    
    title = discord.Embed(title="Titulo del paste", 
                            description=f"{name}", 
                            color=discord.Color.green()
                            )
    version = discord.Embed(title="Version", 
                            description=f"{fansub}", 
                            color=discord.Color.green()
                            )
    msgtitle = await ctx.send(embed=title)
    msgversion = await ctx.send(embed=version)
    
    try:    
        embed = discord.Embed(title="Paste generado", 
                            description=f"El paste ha sido generado correctamente\n\n```{response}```", 
                            color=discord.Color.green()
                            )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await msgtitle.delete()
        await msgversion.delete()
        await msg.delete()
        
    except Exception as e:
        print(e)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.encode('utf-8'))
            temp_file.close()
            file_path = temp_file.name
            msg = await ctx.send(file=discord.File(file_path, "generated_paste.txt"))
            os.remove(file_path)
            await asyncio.sleep(60)
            await msgtitle.delete()
            await msgversion.delete()
            await msg.delete()
    
@commands.has_role(889001453316878367)
@slash.slash(name="newCap",
             description="Genera paste para nuevo capitulo en emision",
             options=[
                 create_option(
                    name="number",
                    description="Numero del capitulo",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="routes",
                    description="Rutas del capitulo",
                    option_type=3,
                    required=True
                ),
             ])
async def newCap(ctx: SlashContext, number, routes):
    from jpawPaste import newemisionCap
    response = await newemisionCap(number, routes)    
    embed = discord.Embed(title="Paste generado", 
                        description=f"El paste ha sido generado correctamente\n\n```{response}```", 
                        color=discord.Color.green()
                        )
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(15)
    await msg.delete()

##################################################################################
#Moderation commands

@slash.slash(name="purge")
async def purge(ctx: SlashContext, amount: int = 1):
    from moderation import clear
    await clear(ctx, amount)
    
    
##################################################################################
#Bot run
bot.run(os.getenv('YUKITEST'))