import asyncio
import logging
import discord
import dotenv
import os
from backend.bot import Bot
from backend.logger import setup_logging

dotenv.load_dotenv()
setup_logging()
bot_token = os.getenv("DISCORD_TOKEN")


bot = Bot(
    command_prefix='!',
    self_bot = True,
    db_path='database/bot.db',
    webhook_url=os.getenv("WEBHOOK_URL"),
    status=discord.Status.online,
)

async def main():
    try:
        logging.info("Memulai koneksi Bot ke Discord...")
        if not bot_token:
            logging.error("DISCORD_TOKEN environment variable is not set.")
            return
        await bot.start(bot_token)
    except discord.ClientException as e:
        logging.error(e)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(bot.closing_bot())
        loop.close()