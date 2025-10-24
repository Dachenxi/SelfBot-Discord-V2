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
        self.bot_embed = EmbedManager(self, webhook_url)
        self.embed_dict = {}
        self.cog_list = ["utility", "idle_miner"]
        self.embed_message = None

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
        logging.info("Loading cog...")
        await self.load_cog()
        logging.info("All Cog loaded.")
        logging.info("Load the embed...")
        self.embed_dict = {
            "author": {
                "name": self.user.name,
                "icon_url": self.user.display_avatar.url
            },
            "title": "**Discord V2 Status**",
            "color": 3926819,
            "description": f"Discord Bot V2.0 dibuat bertujuan untuk membantu Pengguna mengubah akun menjadi sebuah aplikasi yang bisa menjalankan pesan otomatis bahkan online 24 jam",
            "footer": {
                "text": "Discord Bot V2.0 | By Dachenxi",
                "icon_url": self.user.display_avatar.url
            },
            "image": "https://i.ibb.co.com/V0WfzRRf/standard.gif",
            "fields": [
                {
                    "name": "🕹️ *Client Status* 🟢",
                    "value": f"```"
                             f"🕛 Created At    : {self.user.created_at.strftime("%A %B %Y")}\n"
                             f"⭐ Discriminator : {self.user.discriminator}\n"
                             f"🧑‍🌾 Display Name  : {self.user.display_name}\n"
                             f"🌍 Global Name   : {self.user.global_name}\n"
                             f"👤 User ID       : {self.user.id}\n"
                             f"💵 Premium       : {"Tidak Berlangganan Nitro" if not self.user.premium else "Berlangganan Nitro"}\n"
                             f"💲 Premium Type  : {"" if self.user.premium_type.name == "none" else self.user.premium_type.name}```"
                },
                {
                    "name": "🔧 *Command*",
                    "value": f"*Utility*\n"
                             f"{self.command_prefix}reload\n"
                             f"-# Reload semuaa cog/command\n"
                             f"{self.command_prefix}ping\n"
                             f"-# Cek latency bot"
                },
                {
                    "name": "🔧 *Command*",
                    "value": f"*Idle Miner*\n"
                             f"{self.command_prefix}idleminerautoplay | imap\n"
                             f"-# Memulai Otomatisasi Idle Miner\n"
                             f"{self.command_prefix}idleminerautojob | imaj\n"
                             f"-# Memulai dan menghentikan Otomatisasi Job (hunt/fish) Idle Miner\n"
                             f"{self.command_prefix}idleminerautofarm | imaf <crops>\n"
                             f"-# Memulai dan menghentikan otomatisasi farm"
                },
                {
                    "name": "⚙️ **Job Status**",
                    "value": "⛏️ **__Idle Miner__**\n"
                             "***Auto Play*** : 🔴 Not Running\n"
                             "***Auto Job*** : 🔴 Not Running\n"
                             "***Auto Farm*** : 🔴 Not Running\n",
                    "inline": True
                },
                {
                    "name": "⚙️ **Job Status**",
                    "value": "🎣 **__Virtual Fisher__**\n"
                             "***Auto Play*** : 🔴 Not Running\n"
                             "***Auto Upgrade*** : 🔴 Not Running",
                    "inline": True
                }

            ]
        }
        self.embed_message = await self.bot_embed.create_embed(self.embed_dict)
        logging.info("Setup is done")

    async def update_task_status(self,
                                 task_type: Literal["Auto Play", "Auto Job", "Auto Farm", "Auto Upgrade"],
                                 task_name: Literal["Idle Miner", "Virtual Fisher"],
                                 task_status: Literal["Running", "Not Running"]):

        target_field_name = "⚙️ **Job Status**"

        for field in self.embed_dict["fields"]:
            if field.get("name") == target_field_name and task_name in field.get("value", ""):

                lines = field["value"].split("\n")
                for i, line in enumerate(lines):
                    if task_type in line:
                        status_icon = "🟢" if task_status == "Running" else "🔴"
                        lines[i] = f"***{task_type}*** : {status_icon} {task_status}"
                        break

                field["value"] = "\n".join(lines)
                break

        if self.embed_message:
            await self.bot_embed.edit_embed(self.embed_message, self.embed_dict)
            logging.info(f"Updated {task_name} - {task_type} to {task_status}")


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
        await self.close()
        logging.warning("Bot has been closed.")


        
