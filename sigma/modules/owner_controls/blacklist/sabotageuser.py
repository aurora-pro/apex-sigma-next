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
from sigma.core.mechanics.payload import CommandPayload


async def sabotageuser(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        target_id = None
        if pld.args[0].isdigit():
            target_id = int(pld.args[0])
        if target_id:
            if target_id not in cmd.bot.cfg.dsc.owners:
                target = await cmd.bot.get_user(target_id)
                if target:
                    sabotage_file = await cmd.db.is_sabotaged(target.id)
                    if sabotage_file:
                        icon, result, status = '🔓', 'unsabotaged', False
                    else:
                        icon, result, status = '🔒', 'sabotaged', True
                    await cmd.db.set_profile(target.id, 'sabotaged', status)
                    response = discord.Embed(color=0xFFCC4D, title=f'{icon} {target.name} has been {result}.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 No user with that ID was found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ That target is immune.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid user ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing user ID.')
    await pld.msg.channel.send(embed=response)
