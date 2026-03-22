import backend
import discord
import re
import logging
import os
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from discord.ext import commands, tasks

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

        # Gabungkan hasil satu per satu menjadi satu string besar
        final_output = ""
        for team, rank, nick, message in matches:
            safe_message = message.replace("@everyone", "everyone").replace("@here", "here")
            display_team = f"[{team}]" if team else "[—]"
            display_rank = rank if rank else "Explorer"

            # Susun baris per baris
            line = f"{display_team} | `Rank: {display_rank}` | `{nick}`: {safe_message}\n"
            final_output += line

        return final_output.strip()

    @staticmethod
    async def send_webhook(message: str):
        webhook = AsyncDiscordWebhook(url= os.getenv("CHAT_WEBHOOK"), rate_limit_retry=True, content= message)
        await webhook.execute()

    @staticmethod
    async def send_embed(message: discord.Message, url: str, tipe: str = "chat"):
        webhook = AsyncDiscordWebhook(url=url)
        discord_embed = DiscordEmbed()
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
                if tipe == "Auction" and "ꜱᴘᴀᴡɴᴇʀ" in embeds.author.name:
                    discord_embed.add_embed_field(name="Tag", value="<@&1483644297894035569>", inline=False)
            if embeds.footer.text:
                discord_embed.set_footer(text=embeds.footer.text, icon_url=embeds.footer.icon_url)
        webhook.add_embed(discord_embed)
        await webhook.execute()
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == int(os.getenv("CHAT_ID")):
            if message.author.bot:
                if message.content:
                    try:
                        formatted_message = self.format_discord_chat(message.content)
                        await self.send_webhook(formatted_message)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")
                else:
                    try:
                        await self.send_embed(message, os.getenv("CHAT_WEBHOOK"))
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")
        if message.channel.id == int(os.getenv("AUCTION_ID")):
            if message.author.bot:
                try:
                    await self.send_embed(message, os.getenv("AUCTION_WEBHOOK"), "Auction")
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

        if message.channel.id == int(os.getenv("MEMBER_LOG")):
            if message.author.bot:
                try:
                    if "first time" in message.embeds[0].author.name:
                        await self.send_embed(message, os.getenv("MEMBER_WEBHOOK"))
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Sniff(bot))