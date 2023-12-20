import os
import mysql.connector
from discord_webhook import DiscordWebhook, DiscordEmbed

async def update_status_in_db(database, table, name, n_epi, prev_done):
    cursor = database.cursor()
    query = f"UPDATE {table} SET listo = %s WHERE alias = %s AND episodio = %s"
    cursor.execute(query, (prev_done, name, n_epi))
    database.commit()
    cursor.close()

async def send_status_embed(ctx, name, n_epi, action, status_emoji, prev_done, image_url, webhook):
    embed = DiscordEmbed(title=f'• {name}.', color=int('7997191'))
    embed.add_embed_field(name=f'‣ Episodio {n_epi}: {action} {status_emoji}', value=f'{prev_done}', inline=False)
    embed.set_thumbnail(url=image_url)
    webhook = DiscordWebhook(webhook, username='Estado de proyectos - UnsyncSubs', avatar_url='https://cdn.discordapp.com/attachments/1032453549940035587/1036097508423782431/p_003_1.jpg')
    webhook.add_embed(embed)
    response = webhook.execute()
    webhook.remove_embeds()

async def add_show_to_db(database, table, titulo, alias, episodio, listo, imagen, webhook):
    cursor = database.cursor()
    query = "INSERT INTO `%s` (titulo, alias, episodio, listo, imagen, webhook) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (table, titulo, alias, episodio, listo, imagen, webhook))
    database.commit()
    cursor.close()
    
async def save_server_id_to_db(db, server_id, server_name):
    query = "SELECT ServerId FROM serverids WHERE ServerId = %s"
    cursor = db.cursor()
    cursor.execute(query, (server_id,))
    result = cursor.fetchall()
    if not result:
        query = "INSERT INTO serverids (ServerName, ServerId) VALUES (%s, %s)"
        cursor.execute(query, (server_name, server_id))
        db.commit()
        cursor.close()
        return True
    cursor.close()
    return False
        

async def create_table_w_server_name(db, server_name):
    cursor = db.cursor()
    table = '{}_anime'.format(server_name)
    query = "SHOW TABLES LIKE %s"
    cursor.execute(query, (table,))
    result = cursor.fetchone()
    if result:
        await print(f"Table {table} already exists.")
    else:
        query = "USE `hime`; CREATE TABLE `%s` (`titulo` varchar(500) NOT NULL, `alias` varchar(500) NOT NULL, `episodio` int(10) NOT NULL, `listo` varchar(255) NOT NULL, `imagen` mediumtext NOT NULL, `webhook` longtext NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
        cursor.execute(query, (table,))
        db.commit()
        print(f"Table {table} created.")
    cursor.close()

async def check_db_info(ctx, table):
    with mysql.connector.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME')
    ) as db:
        cursor = db.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        result = cursor.fetchall()
        await ctx.send(result)