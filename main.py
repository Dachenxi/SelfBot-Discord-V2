import asyncio
import logging
import discord
import dotenv
import os
from backend.bot import Bot
from backend.logger import setup_logging

dotenv.load_dotenv()
setup_logging()

bot = Bot(
    command_prefix='!',
    self_bot = True,
    db_path='database/bot.db',
    webhook_url=os.getenv("WEBHOOK_URL"),
    activity = discord.Activity(
        application_id = 688591619217293401,
        name = "Discord V2",
        assets = {
            "large_image": "1429834224516595712",
            "large_text": "Discord V2",
        },
        type = discord.ActivityType.streaming,
        state = "By DaChenxi",
        details = "In Development",
    ),
    status=discord.Status.online,
)

async def main():
    try:
        logging.info("Memulai koneksi Bot ke Discord...")
        await bot.start(os.getenv("DISCORD_TOKEN"))
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