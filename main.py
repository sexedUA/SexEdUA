import asyncio
from main_bot import dp
from admin_bot import dp as dp_admin


async def run_bots():
    tasks = [
        asyncio.create_task(dp.start_polling()),
        asyncio.create_task(dp_admin.start_polling())
    ]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run_bots())
