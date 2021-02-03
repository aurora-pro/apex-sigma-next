﻿"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sigma.core.utilities.generic_responses import GenericResponse


async def eject(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        try:
            target = await cmd.bot.get_guild(int(''.join(pld.args)))
            if target:
                await target.leave()
                response = GenericResponse(f'Ejected from {target.name}.').ok()
            else:
                response = GenericResponse('No guild with that ID was found.').not_found()
        except ValueError:
            response = GenericResponse('Invalid guild ID.').error()
    else:
        response = GenericResponse('Missing guild ID.').error()
    await pld.msg.channel.send(embed=response)
