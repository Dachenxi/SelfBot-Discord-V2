import discord
import logging
import datetime
from typing import Literal
from backend.embed import EmbedManager
from database.connection import Database
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, db_path, webhook_url, *args, **kwargs):
        commands.Bot.__init__(self, *args, **kwargs)
        self.database = Database(db_path=db_path)
        self.embed_dict = {}
        self.cog_list = ["utility", "idle_miner", "sniff"]
        self.embed_message = None
        self.owner: discord.User | None = None

    async def parse_msg(self, message: discord.Message):
        if (
            message.author.id == self.user.id and
            message.content.startswith(self.command_prefix)
            ):
            async with message.channel.typing():
                try:
                    await message.delete()
                    parts = message.content[1:].split()
                    command_name = parts[0]
                    command = self.get_command(command_name)
                    ctx = await self.get_context(message)
                    if command:
                        try:
                            args = parts[1] if len(parts) > 1 else ''
                            if args:
                                await command(ctx, args)
                                logging.info(f'Mendapat command {command_name} dengan args {args}')
                            else:
                                await command(ctx)
                                logging.info(f'Mendapat command {command_name} ')
                        except Exception as e:
                            print(f"Error executing command '{command_name}': {e}")
                except Exception as e:
                    print(f"Error processing message: {e}")

    async def on_message(self, message: discord.Message):
        await self.parse_msg(message)
    
    async def on_ready(self):
        logging.info(f'Bot connected as {self.user} (ID: {self.user.id})')

    async def load_cog(self):
        for cog in self.cog_list:
            await self.load_extension('backend.commands.' + cog)
            logging.info(f'Loaded Cog: {cog}')

    async def setup_hook(self):
        logging.info("Starting up the bot...")
        logging.info("Get Owner Object...")
        logging.info("Loading cog...")
        await self.load_cog()
        logging.info("All Cog loaded.")
        logging.info("Load the embed...")
        logging.info("Setup is done")

    async def closing_bot(self):
        logging.info("Closing the bot...")

        if self.embed_message:
            try:
                await self.embed_message.delete()
                logging.info("Embed Message Deleted.")
            except Exception as e:
                logging.error(f"Error deleting message embed: {e}")

        await self.database.close()
        logging.info("Database connection closed.")
        await self.change_presence(status=discord.Status.offline)
        await self.close()
        logging.warning("Bot has been closed.")


        
