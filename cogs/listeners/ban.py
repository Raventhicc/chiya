import logging
import time
from typing import Union

import discord
from discord.ext import commands

from utils import database


log = logging.getLogger(__name__)


class BanListener(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        ban_entry = await guild.fetch_ban(user)
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()[0]
        if logs.user != self.bot.user:
            db = database.Database().get()
            db["mod_logs"].insert(dict(
                user_id=user.id,
                mod_id=logs.user.id,
                timestamp=int(time.time()),
                reason=ban_entry.reason,
                type="ban"
            ))
            db.commit()
            db.close()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(BanListener(bot))
    log.info("Listener loaded: ban")
