import sqlite3 as sq

db = sq.connect("kamasutra.db")
cur = db.cursor()


async def db_start():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS accounts("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "cart_id TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS position("
        "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT,"
        "desc TEXT, "
        "photo TEXT) "
    )

    db.commit()
