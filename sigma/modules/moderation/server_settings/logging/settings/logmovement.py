# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord

from sigma.core.mechanics.command import SigmaCommand


async def logmovement(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_guild:
        log_event = await cmd.db.get_guild_settings(message.guild.id, 'LogMovement')
        if log_event:
            result = 'disabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogMovement', False)
        else:
            result = 'enabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogMovement', True)
        response = discord.Embed(color=0x77B255, title=f'✅ Movement logging {result}.')
    else:
        response = discord.Embed(color=0xBE1931, title='⛔ Access Denied. Manage Server needed.')
    await message.channel.send(embed=response)
