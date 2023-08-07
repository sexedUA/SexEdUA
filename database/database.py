import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect("kamasutra.db")
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS accounts("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "tg_id INTEGER, "
        "cart_id TEXT)"
    )
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS positions("
        "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "   
        "desc TEXT, "
        "photo BLOB )")
    db.commit()

async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()


        
async def  add_item(state):
    async with state.proxy() as data:
        connection = sq.connect("kamasutra.db")
        cur = connection.cursor()
        cur.execute("INSERT INTO positions (desc, photo) VALUES (?, ?)",
                        (data['desc'], data['photo']))
        connection.commit()
        connection.close()


def get_positions():
    connection = sq.connect("kamasutra.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM positions")
    items_data = cur.fetchall()
    connection.close()
    return items_data


# connection = sq.connect("kamasutra.db")
# cur = connection.cursor()
# cur.execute('DELETE FROM positions')
# connection.commit()
# connection.close()

