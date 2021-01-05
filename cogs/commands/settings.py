import logging

from discord.ext import commands

from utils.record import record_usage

log = logging.getLogger(__name__)


class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.before_invoke(record_usage)
    @commands.group()
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('No settings subcommand specified.')


def setup(bot) -> None:
    """Load the SettingsCog cog."""
    bot.add_cog(SettingsCog(bot))
    log.info("Cog loaded: SettingsCog")
