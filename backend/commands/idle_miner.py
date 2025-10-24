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
        self.upgrade_cycler = itertools.cycle(["pickaxe", "backpack"])
        self.dict_command: dict[str, discord.SlashCommand | None] = {
            "sell" : None,
            "upgrade" : None,
            "rebirth" : None,
            "prestige" : None,
            "hunt": None,
            "fish": None,
            "plant": None,
            "farm": None,
        }

    @tasks.loop(seconds=1)
    async def auto_play(self, channel: discord.TextChannel):
        try:
            upgrade_type = next(self.upgrade_cycler)
            for i in range(random.randint(1, 10)):
                await self.dict_command["sell"].__call__(channel)
                await  asyncio.sleep(random.randint(3, 6))
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

    @tasks.loop(seconds=1)
    async def auto_job(self, channel: discord.TextChannel):
        try:
            await self.dict_command["hunt"].__call__(channel)
            await asyncio.sleep(random.randint(5, 10))
            await self.dict_command["fish"].__call__(channel)
            await asyncio.sleep(5 * 60 + random.randint(5, 15))
        except Exception as e:
            logging.error(f"Error in auto_job task: {e}")

    @tasks.loop(seconds=1)
    async def auto_farm(self, channel: discord.TextChannel, plant: str = "Carrot"):
        try:
            await self.dict_command["plant"].__call__(channel, area="all", crop=plant)
            await asyncio.sleep(random.randint(1, 3))
            farm_interaction = await self.dict_command["farm"].__call__(channel)
            farm_message = await channel.fetch_message(farm_interaction.message.id)

            total_seconds = 0
            for embed in farm_message.embeds:
                time_pattern = r"crop ready in (?:(\d+)h)?\s?(?:(\d+)m)?\s?(?:(\d+)s)?"
                time_search = re.search(time_pattern, embed.description)

                if time_search:
                    hours, minutes, seconds = time_search.groups()

                    if hours:
                        total_seconds += int(hours) * 3600
                    if minutes:
                        total_seconds += int(minutes) * 60
                    if seconds:
                        total_seconds += int(seconds)

            await asyncio.sleep(total_seconds + random.randint(5, 15))
        except Exception as e:
            logging.error(f"Error in auto_far task: {e}")

    async def get_command(self, channel: discord.TextChannel):
        if all(cmd is None for cmd in self.dict_command.values()):
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
                elif slash.id == 958125966171967578:
                    self.dict_command["hunt"] = slash
                elif slash.id == 958125967061184593:
                    self.dict_command["fish"] = slash
                elif slash.id == 968186271971287110:
                    self.dict_command["plant"] = slash
                elif slash.id == 968186270197121044:
                    self.dict_command["farm"] = slash
                if all(cmd is not None for cmd in self.dict_command.values()):
                    break

    @commands.command(name="idleminerautoplay", aliases=["imap"])
    async def idle_miner_auto_play(self, ctx: commands.Context):
        await self.get_command(ctx.channel)
        if self.auto_play.is_running():
            self.auto_play.cancel()
            await ctx.send("Idle Miner Auto Play stopped.")
            await self.bot.update_task_status(task_type="Auto Play", task_name="Idle Miner", task_status="Not Running")
            return

        self.auto_play.start(ctx.channel)
        await ctx.send("Idle Miner Auto Play started.")
        await self.bot.update_task_status(task_type="Auto Play", task_name="Idle Miner", task_status="Running")

    @commands.command(name="idleminerautojob", aliases=["imaj"])
    async def idle_miner_auto_job(self, ctx: commands.Context):
        await self.get_command(ctx.channel)
        if self.auto_job.is_running():
            self.auto_job.cancel()
            await ctx.send("Idle Miner Auto Job stopped.")
            await self.bot.update_task_status(task_type="Auto Job", task_name="Idle Miner", task_status="Not Running")
            return

        self.auto_job.start(ctx.channel)
        await ctx.send("Idle Miner Auto Jon started.")
        await self.bot.update_task_status(task_type="Auto Job", task_name="Idle Miner", task_status="Running")

    @commands.command(name="idleminerautofarm", aliases=["imaf"])
    async def idle_miner_auto_farm(self, ctx: commands.Context, crops:str):
        await self.get_command(ctx.channel)
        if self.auto_farm.is_running():
            self.auto_farm.cancel()
            await ctx.send("Idle Miner Auto Farm stopped.")
            await self.bot.update_task_status(task_type="Auto Farm", task_name="Idle Miner", task_status="Not Running")
            return

        self.auto_farm.start(ctx.channel, crops)
        await ctx.send("Idle Miner Auto Farm started.")
        await self.bot.update_task_status(task_type="Auto Farm", task_name="Idle Miner", task_status="Running")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None and message.author.id == 518759221098053634:
            self.auto_play.cancel()
            self.auto_job.cancel()
            await self.bot.update_task_status(task_type="Auto Play", task_name="Idle Miner", task_status="Not Running")
            await self.bot.update_task_status(task_type="Auto Job", task_name="Idle Miner", task_status="Not Running")




async def setup(bot: backend.bot.Bot):
    await bot.add_cog(IdleMiner(bot))