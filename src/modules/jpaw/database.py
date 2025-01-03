import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('LOCAL_HOST'),
    port=int(os.getenv('LOCAL_PORT')),
    user=os.getenv('LOCAL_USER'),
    password=os.getenv('LOCAL_PASSWORD'),
    database=os.getenv('LOCAL_NAME')
)
cursor = db.cursor()


async def new_paste(
    name = None,
    mirror1 = None,
    mirror2 = None,
    mirror3 = None,
    mirror4 = None,
    mirror5 = None,
    mirror6 = None,
    fansub1 = None,
    fansub2 = None,
    fansub3 = None,
    fansub4 = None,
    fansub5 = None,
    fansub6 = None,
    ):
    """
    Inserts a new paste entry into the database and returns the ID of the newly created paste.
    Args:
        name (str, optional): The title of the paste.
        mirror1 (str, optional): URL for the first mirror.
        mirror2 (str, optional): URL for the second mirror.
        mirror3 (str, optional): URL for the third mirror.
        mirror4 (str, optional): URL for the fourth mirror.
        mirror5 (str, optional): URL for the fifth mirror.
        mirror6 (str, optional): URL for the sixth mirror.
        fansub1 (str, optional): Name for the first fansub.
        fansub2 (str, optional): Name for the second fansub.
        fansub3 (str, optional): Name for the third fansub.
        fansub4 (str, optional): Name for the fourth fansub.
        fansub5 (str, optional): Name for the fifth fansub.
        fansub6 (str, optional): Name for the sixth fansub.
    Returns:
        int: The ID of the newly created paste.
    """
    query = (
        "INSERT INTO `pastes`"
        + "(`id`, `pass`, `title`, `create_at`, `Mirror1`, `Mirror2`, `Mirror3`, `Mirror4`, `Mirror5`, `Mirror6`,"
        + "`Mname1`, `Mname2`, `Mname3`, `Mname4`, `Mname5`, `Mname6`, `views`, `user_id`, `reported`, `vip`)"
        + "VALUES (NULL, NULL, %s, current_timestamp(), %s, %s, %s, %s, %s, %s,"
        + "%s, %s, %s, %s, %s, %s, 0, 74, 0, 0);"
        ).encode("utf-8")
    cursor.execute(query, (name, mirror1, mirror2, mirror3, mirror4, mirror5, mirror6, fansub1, fansub2, fansub3, fansub4, fansub5, fansub6))
    db.commit()
    query = "select id from `pastes` where title = %s;"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    return result[0]
    
    
async def search_anime(anime=None):
    """
    Searches for anime titles in the database that match the given keyword.

    Args:
        anime (str, optional): The keyword to search for in anime titles. Defaults to None.

    Returns:
        list: A list of tuples containing the id and title of the matching anime.
    """
    query = f"select id, title from `pastes` where title like '%{anime}%';"
    cursor.execute(query)
    return cursor.fetchall()

def add_version():
    pass

def select_paste():
    pass

if __name__ == '__main__':
    result = search_anime(anime='hori')
    for item in result:
        print(f'[{item[1]}](https://paste.japan-paw.net/?v={item[0]})')