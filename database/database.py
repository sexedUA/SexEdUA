import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect("kamasutra.db")
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "tg_id INTEGER, "
        "cart_id TEXT, "
        "age INTEGER, "
        "gender INTEGER, "
        "orientation INTEGER) "
    )
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS positions("
        "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "desc TEXT, "
        "photo BLOB )")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS stories("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "text TEXT, "
        "status TEXT )")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS reviews("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "desc TEXT, "
        "link TEXT,  "
        "photo BLOB,  "
        "file_id TEXT)")
    db.commit()


async def cmd_start_db(user_id, age, gender, orientation):
    user = cur.execute("SELECT * FROM users WHERE tg_id = ?",
                        (user_id,)).fetchone()

    if not user:
        cur.execute("INSERT INTO users (tg_id, age, gender, orientation) VALUES (?, ?, ?, ?)",
                        (user_id, age, gender, orientation))
        db.commit()

def get_user(user_id):
    connection = sq.connect("kamasutra.db")
    cur.execute("SELECT * FROM users WHERE tg_id = ?", (user_id,))
    user = cur.fetchone()
    connection.close()
    return user


async def add_item(state):
    async with state.proxy() as data:
        connection = sq.connect("kamasutra.db")
        cur = connection.cursor()
        cur.execute("INSERT INTO positions (desc, photo) VALUES (?, ?)",
                    (data['desc'], data['photo']))
        connection.commit()
        connection.close()

async def add_review(state):
    async with state.proxy() as data:
        connection = sq.connect("kamasutra.db")
        cur = connection.cursor()
        cur.execute("INSERT INTO reviews (desc, link,  photo) VALUES (?, ?, ?)",
                    (data['desc'], data['link'], data['photo']))
        connection.commit()
        connection.close()


def get_positions():
    connection = sq.connect("kamasutra.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM positions")
    items_data = cur.fetchall()
    connection.close()
    return items_data


def get_review():
    connection = sq.connect("kamasutra.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM reviews")
    photo_data = cur.fetchall()
    connection.close()
    return photo_data


def get_stories():
    connection = sq.connect("kamasutra.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM stories WHERE status == 'active'")
    items_data = cur.fetchall()
    connection.close()
    return items_data


async def add_story(state):
    async with state.proxy() as data:
        connection = sq.connect("kamasutra.db")
        cur = connection.cursor()
        cur.execute("INSERT INTO stories (text, status) VALUES (?, ?)",
                    (data["text"], 'inactive'))
        connection.commit()
        connection.close()


# connection = sq.connect("kamasutra.db")
# cur = connection.cursor()
# cur.execute('DELETE FROM reviews WHERE id=6')
# connection.commit()
# connection.close()

# connection = sq.connect("kamasutra.db")
# cur = connection.cursor()
# cur.execute("DROP TABLE IF EXISTS reviews")
# connection.commit()
# connection.close()