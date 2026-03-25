import datetime
import backend
import discord
import re
import logging
import os
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from discord.ext import commands

logging.getLogger("httpx").setLevel(logging.WARNING)


class Sniff(commands.Cog):
    def __init__(self, bot: backend.bot.Bot):
        self.bot = bot

    @staticmethod
    def format_discord_chat(text):
        # Regex yang menangkap Team, Rank (opsional), Nickname, dan Pesan
        pattern = r"\[(.*?)\]\s+(?:\**(\w+)\**\s+)?([^\s»]+)\s*»\s*(.*)"

        # Mencari semua kecocokan
        matches = re.findall(pattern, text)

        for team, rank, nick, message in matches:
            safe_message = message.replace("@everyone", "everyone").replace("@here", "here")
            display_team = f"{team}" if team else "None"
            display_rank = rank if rank else "Explorer"
            return {"team": display_team,"rank":display_rank,"nick":nick.replace('\\', ''),"message":safe_message}
        return None

    @staticmethod
    async def send_webhook(nick:str, rank: str, team: str, message: str):
        webhook = AsyncDiscordWebhook(url= os.getenv("CHAT_WEBHOOK"), rate_limit_retry=True)
        embed = DiscordEmbed()
        embed.set_author(name=nick)
        embed.set_description(f"`Rank: {rank}` | `Team: {team}`: {message}")
        embed.set_footer(text=f"Chat In Game")
        embed.set_timestamp(datetime.datetime.now(datetime.UTC).isoformat())
        embed.set_color(color=discord.Color.dark_blue().value)
        webhook.add_embed(embed)
        await webhook.execute()

    @staticmethod
    async def send_embed(message: discord.Message, url: str, tipe: str = "chat"):
        webhook = AsyncDiscordWebhook(url=url)
        discord_embed = DiscordEmbed()
        chat_webhook = None
        for embeds in message.embeds:
            if embeds.author.name:
                discord_embed.set_author(name=embeds.author.name, url=embeds.author.url, icon_url=embeds.author.icon_url)
            if embeds.title:
                discord_embed.set_title(title=embeds.title)
            if embeds.description:
                discord_embed.set_description(description=embeds.description)
            if embeds.image.url:
                discord_embed.set_image(url=embeds.image.url)
            if embeds.thumbnail.url:
                discord_embed.set_thumbnail(url=embeds.thumbnail.url)
            if embeds.color:
                discord_embed.set_color(color=embeds.color.value)
            if embeds.fields:
                for field in embeds.fields:
                    discord_embed.add_embed_field(name=field.name, value=field.value, inline=True)
                if tipe == "Auction" and "ꜱᴘᴀᴡɴᴇʀ" in embeds.author.name and "selling" in embeds.author.name:
                    chat_webhook = AsyncDiscordWebhook(url=os.getenv("CHAT_WEBHOOK"), content="<@&1483644297894035569>")
            if embeds.footer.text:
                discord_embed.set_footer(text=embeds.footer.text, icon_url=embeds.footer.icon_url)
            discord_embed.set_timestamp(datetime.datetime.now(datetime.UTC).isoformat())
        webhook.add_embed(discord_embed)
        await webhook.execute()
        if chat_webhook:
            await chat_webhook.execute()

    @staticmethod
    async def send_chat_embed(message: discord.Message, url: str):
        webhook = AsyncDiscordWebhook(url=url)
        discord_embed = DiscordEmbed()
        discord_embed.set_author(name=f"{message.author.name}{" | "+ message.author.display_name if message.author.display_name else ""}")
        discord_embed.set_description(message.content)
        discord_embed.set_footer(text=f"Chat from discord")
        discord_embed.set_timestamp(datetime.datetime.now(datetime.UTC).isoformat())
        discord_embed.set_color(color=discord.Color.dark_orange().value)
        webhook.add_embed(discord_embed)
        await webhook.execute()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == int(os.getenv("CHAT_ID")):
            if message.author.bot:
                if message.content:
                    try:
                        split_message = self.format_discord_chat(message.content)
                        await self.send_webhook(split_message["nick"], split_message["rank"], split_message["team"], split_message["message"])
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")
            else:
                try:
                    await self.send_chat_embed(message, os.getenv("CHAT_WEBHOOK"))
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
        if message.channel.id == int(os.getenv("AUCTION_ID")):
            if message.author.bot:
                try:
                    await self.send_embed(message, os.getenv("AUCTION_WEBHOOK"), "Auction")
                    logging.info("Sending Auction Embed")

                except Exception as e:
                    logging.error(f"Error processing message: {e}")

        if message.channel.id == int(os.getenv("MEMBER_LOG")):
            if message.author.bot:
                try:
                    if "first time" in message.embeds[0].author.name:
                        await self.send_embed(message, os.getenv("MEMBER_WEBHOOK"))
                    else:
                        await self.send_embed(message, os.getenv("JOIN_LEAVE_WEBHOOK"))
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Sniff(bot))