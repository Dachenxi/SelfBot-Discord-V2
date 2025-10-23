import backend
import discord
import itertools
import re
import random
import asyncio
import logging
from discord.ext import commands, tasks

class IdleMiner(commands.Cog):
    def __init__(self, bot: backend.bot.Bot):
        self.bot = bot
        self.dict_command: dict[str, discord.SlashCommand | None] = {
            "sell" : None,
            "upgrade" : None,
            "rebirth" : None,
            "prestige" : None,
        }

    @tasks.loop(seconds=1)
    async def auto_play(self, channel: discord.TextChannel):
        try:
            upgrade_type = next(itertools.cycle(["pickaxe", "backpack"]))
            await self.dict_command["sell"].__call__(channel)
            backpack_interaction = await self.dict_command["upgrade"].__call__(channel, item=upgrade_type, amount="all")
            backpack_message = await channel.fetch_message(backpack_interaction.message.id)
            time = re.search(r"BP:(?:(\d+)m)?(?:(\d+)s)?", backpack_message.content)
            total_delay = 0
            if time:
                minutes_str = time.group(1)
                seconds_str = time.group(2)

                if minutes_str:
                    total_delay += int(minutes_str) * 60
                if seconds_str:
                    total_delay += int(seconds_str)

            if "rebirth" in backpack_message.content:
                await self.dict_command["rebirth"].__call__(channel)
                await asyncio.sleep(random.randint(5, 15))
            elif "prestige" in backpack_message.content:
                await self.dict_command["prestige"].__call__(channel)
                await asyncio.sleep(random.randint(5, 15))
            elif "can't afford" in backpack_message.content:
                await asyncio.sleep(random.randint(300, 360))

            await asyncio.sleep(total_delay + random.randint(5, 15))

        except Exception as e:
            logging.error(f"Error in auto_play task: {e}")

    async def get_command(self, channel: discord.TextChannel):
        list_slashcommand = await channel.application_commands()
        for slash in list_slashcommand:
            if slash.id == 958128515797106738:
                self.dict_command["sell"] = slash
            elif slash.id == 968191331807658046:
                self.dict_command["upgrade"] = slash
            elif slash.id == 958127513870159873:
                self.dict_command["rebirth"] = slash
            elif slash.id == 958128104591740981:
                self.dict_command["prestige"] = slash
            if all(cmd is not None for cmd in self.dict_command.values()):
                break

    @commands.command(name="idleminerautoplay", aliases=["imap"])
    async def idle_miner_auto_play(self, ctx: commands.Context):
        await self.get_command(ctx.channel)
        if all(cmd is not None for cmd in self.dict_command.values()):
            if self.auto_play.is_running():
                self.auto_play.stop()
                await ctx.send("Idle Miner Auto Play stopped.")
                await self.bot.update_task_status(task_type="Auto Play", task_name="Idle Miner", task_status="Not Running")
            else:
                self.auto_play.start(ctx.channel)
                await ctx.send("Idle Miner Auto Play started.")
                await self.bot.update_task_status(task_type="Auto Play", task_name="Idle Miner", task_status="Running")
        else:
            await ctx.send("Failed to retrieve all necessary commands.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None and message.author.id == 518759221098053634:
            self.auto_play.stop()
            await self.bot.update_task_status(task_type="Auto Play", task_name="Idle Miner", task_status="Not Running")




async def setup(bot: backend.bot.Bot):
    await bot.add_cog(IdleMiner(bot))