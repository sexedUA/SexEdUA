import os
import libsql_client
import uuid
import logging


client = libsql_client.create_client_sync(
    url=os.getenv("TURS0_URL"), auth_token=os.getenv("TURSO_TOKEN")
)


async def db_start():
    client.execute(
        """CREATE TABLE IF NOT EXISTS consultings (
               id UUID PRIMARY KEY,
               phone TEXT,
               status BOOLEAN DEFAULT False
           )"""
    )


async def db_close():
    client.close()


async def cmd_start_db(user_id, age, gender, orientation):
    rs = client.execute(f"select * from users where tg_id == {user_id}")
    user = rs.rows
    if not user:
        client.execute(
            "insert into users values (:uid, :tg_id, :age, :gender, :orientation)",
            {
                "uid": f"{uuid.uuid4()}",
                "tg_id": user_id,
                "age": age,
                "gender": gender,
                "orientation": orientation,
            },
        )


def get_user(user_id):
    rs = client.execute(f"select * from users where tg_id == {user_id}")
    return rs.rows


async def add_item(state):
    async with state.proxy() as data:
        client.execute(
            "insert into positions values (:uid, :description, :photo)",
            {
                "uid": f"{uuid.uuid4()}",
                "description": data["desc"],
                "photo": data["photo"],
            },
        )


async def add_review(state):
    async with state.proxy() as data:
        client.execute(
            "insert into reviews values (:uid, :description, :link, :photo)",
            {
                "uid": f"{uuid.uuid4()}",
                "description": data["desc"],
                "link": data["link"],
                "photo": data["photo"],
            },
        )


def get_positions():
    rs = client.execute("select * from positions")
    return rs.rows


def get_review():
    rs = client.execute("select * from reviews")
    return rs.rows


def get_stories():
    rs = client.execute("select * from stories where status == 1")
    return rs.rows


def get_stories_admin():
    rs = client.execute("select * from stories where status == 0")
    return rs.rows


async def add_story(state):
    async with state.proxy() as data:
        client.execute(
            "insert into stories values (:uid, :content, :status)",
            {"uid": f"{uuid.uuid4()}", "content": data["text"], "status": False},
        )


async def add_consultation(state, phone: str):
    async with state.proxy() as data:
        try:
            await db_start()
            client.execute(
                "INSERT INTO consultings (id, phone, status) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), phone, False),
            )
            logging.info(f"Consultation added with phone {phone}.")
        except Exception as e:
            logging.error(f"Error adding consultation: {e}")


async def update_consultation_status(phone: str, status: bool):
    client.execute("UPDATE consultings SET status = ? WHERE phone = ?", (status, phone))


def get_consultation_requests():
    rs = client.execute("SELECT phone, status FROM consultings")
    return rs.rows


async def add_subscriber(user_id):
    try:
        client.execute("INSERT INTO subscribers (user_id) VALUES (?)", (user_id,))
    except Exception as e:
        if "UNIQUE constraint failed" not in str(e):
            logging.error(f"Error adding user {user_id} to subscribers: {e}")


def get_subscribers():
    query = "SELECT user_id FROM subscribers"
    result = client.execute(query)
    subscribers = [row[0] for row in result.rows]
    return subscribers


def get_story_by_text(text):
    rs = client.execute(f"select id from stories where content == '{text}'")
    return rs.rows


def update_story(uid: str, type: str):
    if type == "approve-story":
        client.execute(f"update stories set status = {True} where id == '{uid}'")
    else:
        client.execute(f"delete from stories where id == '{uid}'")


def get_link():
    rs = client.execute("select * from youtube")
    return rs.rows


async def add_link(state):
    async with state.proxy() as data:
        client.execute(
            "insert into youtube values (:uid, :description, :link)",
            {
                "uid": f"{uuid.uuid4()}",
                "description": data["description"],
                "link": data["link"],
            },
        )


def get_info():
    rs = client.execute("SELECT * FROM consultings")
    return rs.rows


table_info = get_info()
print(table_info)
