import datetime
import discord
import re
import logging
import os
from discord import Embed, Message, Webhook
from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.bot import Bot


logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Sniff(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.user_chat_pattern = r"\[(.*?)\]\s+(?:\**(\w+)\**\s+)?([^\s»]+)\s*»\s*(.*)"

        try:
            self.chat_channel_id = int(os.getenv("CHAT_ID", 0))
            self.auction_channel_id = int(os.getenv("AUCTION_ID", 0))
            self.member_log_channel_id = int(os.getenv("MEMBER_LOG", 0))
        
        except ValueError:
            logger.error("Invalid channel ID di .env file. Pastikan semua channel ID adalah angka yang valid.")

        finally:
            if self.chat_channel_id == 0 or self.auction_channel_id == 0 or self.member_log_channel_id == 0:
                logger.warning("Satu atau lebih channel ID tidak diatur dengan benar. Pastikan CHAT_ID, AUCTION_ID, dan MEMBER_LOG di .env file sudah diisi dengan benar.")

    def format_discord_chat(self, text):
        # Regex yang menangkap Team, Rank (opsional), Nickname, dan Pesan

        # Mencari semua kecocokan
        matches = re.findall(self.user_chat_pattern, text)

        for team, rank, nick, message in matches:
            safe_message = message.replace("@everyone", "everyone").replace("@here", "here")
            display_team = f"{team}" if team else "None"
            display_rank = rank if rank else "Explorer"
            return {
                "team": display_team,
                "rank": display_rank,
                "nick": nick.replace('\\', ''),
                "message": safe_message
            }
        return None

    async def send_chat_webhook(self, nick:str, rank: str, team: str, message: str):
        webhook_url = os.getenv("CHAT_WEBHOOK")
        if not webhook_url:
            logger.error("CHAT_WEBHOOK Environment belum diatur.")
            return
        
        webhook_conn = Webhook.from_url(url=webhook_url, client=self.bot)
        embed = discord.Embed(
            description=f"{message}",
            timestamp=datetime.datetime.now(datetime.UTC),
            color=discord.Color.brand_green()
        )
        embed.set_author(
            name=f"{nick} | {rank} [{team}]",
            icon_url=f"https://mc-heads.net/avatar/{nick}"
            )
        embed.set_footer(text="Chat In Game")

        await webhook_conn.send(
            embed=embed,
        )

    async def send_auction_embed(self, message: discord.Message):
        webhook_url = os.getenv("AUCTION_WEBHOOK")
        if not webhook_url:
            logger.error("AUCTION_WEBHOOK Environment belum diatur.")
            return
        webhook_conn = Webhook.from_url(url=webhook_url, client=self.bot)
        
        author_name = message.embeds[0].author.name if message.embeds and message.embeds[0].author else ""
        if author_name:
            nick = author_name.split(" ")[0]

        for source_embed in message.embeds:
            embed = source_embed.copy()
            embed.timestamp = datetime.datetime.now(datetime.UTC)
        
            author_name = source_embed.author.name or ""
            
            await webhook_conn.send(
                embed=embed,
                username=nick if nick else "Auction Bot",
                avatar_url=f"https://mc-heads.net/avatar/{nick}" if nick else None
            )
    
    async def send_event_embed(self, message: discord.Message, webhook_url: str):
        if not webhook_url:
            logger.error("Event webhook URL environment variable is not set.")
            return
        webhook_conn = Webhook.from_url(url=webhook_url, client=self.bot)
        
        for source_embed in message.embeds:
            embed = source_embed.copy()
            embed.timestamp = datetime.datetime.now(datetime.UTC)
            
            await webhook_conn.send(
                embed=embed
            )

    async def send_discord_chat(self, message: discord.Message):
        """Meneruskan pesan dari sebuah chat di discord

        Args:
            message (discord.Message): pesan dari embed tersebut
        """
        webhook_url = os.getenv("CHAT_WEBHOOK")
        if not webhook_url:
            logger.error("CHAT_WEBHOOK environment variable is not set.")
            return
        
        webhook_conn = Webhook.from_url(url=webhook_url, client=self.bot)
        embed = Embed(
            description=message.content,
            timestamp=datetime.datetime.now(datetime.UTC),
            color=discord.Color.brand_red()
        )
        embed.set_author(
            name=f"{message.author.name}#{message.author.discriminator}",
            icon_url=message.author.avatar.url if message.author.avatar else None
        )


        await webhook_conn.send(
            embed=embed
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == self.chat_channel_id:
            await self._handle_chat_channel(message)
        elif message.channel.id == self.auction_channel_id:
            await self._handle_auction_channel(message)
        elif message.channel.id == self.member_log_channel_id:
            await self._handle_member_log_channel(message)

    async def _handle_chat_channel(self, message:Message):
        """Handle untuk chat channel

        Args:
            message (Message): message dari discord client
        """
        if message.author.bot:
            if not message.content:
                await self.send_event_embed(message, os.getenv("CHAT_WEBHOOK", ""))
                return

            split_message = self.format_discord_chat(message.content)
            if not split_message:
                logger.warning(f"Gagal memparse pesan: {message.content}")
                return

            await self.send_chat_webhook(
                split_message["nick"],
                split_message["rank"],
                split_message["team"],
                split_message["message"],
            )
            return
        else:
            await self.send_discord_chat(message)
    
    async def _handle_auction_channel(self, message:Message):
        """Handle untuk auction channel

        Args:
            message (Message): message dari discord client
        """
        if message.author.bot:
            await self.send_auction_embed(message)
            return
    
    async def _handle_member_log_channel(self, message:Message):
        """Handle untuk member log channel

        Args:
            message (Message): message dari discord client
        """
        if message.author.bot:
            author_name = message.embeds[0].author.name if message.embeds and message.embeds[0].author else ""

            if author_name and "first time" in author_name:
                member_webhook_url = os.getenv("MEMBER_WEBHOOK")
                if not member_webhook_url:
                    logger.error("MEMBER_WEBHOOK environment variable is not set.")
                    return
                await self.send_event_embed(message, member_webhook_url)
            else:
                join_leave_webhook_url = os.getenv("JOIN_LEAVE_WEBHOOK")
                if not join_leave_webhook_url:
                    logger.error("JOIN_LEAVE_WEBHOOK environment variable is not set.")
                    return
                await self.send_event_embed(message, join_leave_webhook_url)
            return

async def setup(bot: "Bot"):
    await bot.add_cog(Sniff(bot))