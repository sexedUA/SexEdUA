import os
import libsql_client
import uuid
import logging


client = libsql_client.create_client_sync(
    url=os.getenv("TURS0_URL"), auth_token=os.getenv("TURSO_TOKEN")
)


async def db_start():
    pass


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


async def add_subscriber(user_id):
    try:
        await client.execute("INSERT INTO subscribers (user_id) VALUES (?)", (user_id,))
        logging.info(f"User {user_id} added to subscribers.")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            logging.info(f"User {user_id} is already a subscriber.")
        else:
            logging.error(f"Error adding user {user_id} to subscribers: {e}")


def get_subscribers():
    query = "SELECT user_id FROM subscribers"
    result = client.execute(query)
    subscribers = [row[0] for row in result.rows]
    return subscribers


def get_info():
    rs = client.execute("SELECT * FROM users")
    return rs.rows


table_info = get_info()
print(table_info)
