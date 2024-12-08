import os, discord, mysql.connector, sys
from discord.ext import commands
from modules.himatimes.db_actions import update_status_in_db, send_status_embed, add_show_to_db

sys.path.append('src/modules/himatimes')

intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix='^', intents=intents)

positions = {key: (f'<:{name}:{id}>', name.replace('_', ' ').title()) for key, (name, id) in {
    'tr': ('Traduccion', '1059298060112507021'),
    'cc': ('Correccion', '1059298054622171207'),
    'ti': ('Tiempos', '1059298058573205545'),
    'ed': ('Edicion', '1059298055951749281'),
    'fx': ('Efectos', '1059308406181199963'),
    'ec': ('Encode', '1059298057201651722'),
    'qc': ('Control_Calidad', '1059298053095444570'),
}.items()}

async def status(ctx, 
                 name: str, 
                 n_epi: int = None, 
                 to_do: str = None, 
                 position: str = None,
                 table: str = None):
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
            query = f"SELECT * FROM {table} WHERE alias = %s AND episodio = {n_epi}"
            cursor.execute(query, (name,))
            rows = cursor.fetchall()
            found_episode = False
            for row in rows:
                if row[1] == name and row[2] == n_epi:
                    found_episode = True
                    prev_done = f'{row[3]} {emoji} ' if to_do.lower() == 'done' else row[3].replace(f'{emoji} ', '')
                    await update_status_in_db(database, table, name, n_epi, prev_done)
                    await send_status_embed(ctx, row[0], n_epi, action, status_emoji, prev_done, row[4], row[5])                
            if not found_episode: 
                query = f"SELECT titulo, alias, imagen, webhook FROM {table} WHERE alias = %s LIMIT 1"
                cursor.execute(query, (name, ))
                result = cursor.fetchaone()
                for row in result:
                    show = row[0]
                    alias = row[1]
                    imagen = row[2]
                    webhook = row[3]
                await ctx.send(f"{show} no tiene el episodio {n_epi} en la base de datos, se agregará ahora.")
                await add_show_to_db(database, table, titulo=show, alias=alias, episodio=n_epi, listo=emoji, imagen=imagen, webhook=webhook)
                await ctx.send(f"El capitulo {n_epi} del anime {name} ha sido agregado a la base de datos.")
                await send_status_embed(ctx, show, n_epi, action, '<a:Listo:1151660812759478342>', emoji, imagen, webhook)
                return True
        except Exception :
            await ctx.send("No se ha encontrado el anime en la base de datos.")
            return False