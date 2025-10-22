import logging
import backend
import random
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot: backend.bot.Bot):
        self.bot = bot

    @commands.command(name="reload cog", aliases=["reload"])
    async def reload_cog(self, ctx: commands.Context):
        for cog in self.bot.cog_list:
            await self.bot.reload_extension('backend.commands.' + cog)
            logging.info(f'Reloaded Cog: {cog}')

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        try:
            await ctx.send(f"Pong {random.randint(1,100)}ms")
        except Exception as e:
            await ctx.send(f"Error {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))