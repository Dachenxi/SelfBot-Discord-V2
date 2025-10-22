import aiosqlite

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_path)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def execute(self, query: str, params: tuple = ()):
        async with self.connection.execute(query, params) as cursor:
            await self.connection.commit()
            return cursor

    async def fetchall(self, query: str, params: tuple = ()):
        async with self.connection.execute(query, params) as cursor:
            return await cursor.fetchall()

    async def fetchone(self, query: str, params: tuple = ()):
        async with self.connection.execute(query, params) as cursor:
            return await cursor.fetchone()