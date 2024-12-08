import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('LOCAL_HOST'),
    port=int(os.getenv('LOCAL_PORT')),
    user=os.getenv('LOCAL_USER'),
    password=os.getenv('LOCAL_PASSWORD'),
    database=os.getenv('LOCAL_DATABASE')
)
cursor = db.cursor()


def new_paste(
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
    
    query = (
        "INSERT INTO `pastes`"
        + "(`id`, `pass`, `title`, `create_at`, `Mirror1`, `Mirror2`, `Mirror3`, `Mirror4`, `Mirror5`, `Mirror6`,"
        + "`Mname1`, `Mname2`, `Mname3`, `Mname4`, `Mname5`, `Mname6`, `views`, `user_id`, `reported`, `vip`)"
        + "VALUES (NULL, NULL, %s, current_timestamp(), %s, %s, %s, %s, %s, %s,"
        + "%s, %s, %s, %s, %s, %s, NULL, NULL, 0, NULL);"
        )
    print(query, (name))
    cursor.execute(query, (name, mirror1, mirror2, mirror3, mirror4, mirror5, mirror6, fansub1, fansub2, fansub3, fansub4, fansub5, fansub6))
    db.commit()
    return 'Commit succeful'
    
def select_version():
    pass

def select_paste():
    pass

if __name__ == '__main__':
    new_paste()