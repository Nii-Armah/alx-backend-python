import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            return await cursor.fetchall()


async def main():
   result = await asyncio.gather(
       async_fetch_users(),
       async_fetch_older_users()
   )
   print(result)

asyncio.run(main())