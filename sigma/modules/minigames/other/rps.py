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

import secrets

import discord

from sigma.core.utilities.generic_responses import GenericResponse


async def rps(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        their_choice, counter = None, None
        sign_list = ['rock', 'paper', 'scissors']
        if pld.args[0].lower().startswith('r'):
            their_choice, counter = 'rock', 'paper'
        elif pld.args[0].lower().startswith('p'):
            their_choice, counter = 'paper', 'scissors'
        elif pld.args[0].lower().startswith('s'):
            their_choice, counter = 'scissors', 'rock'
        if their_choice:
            my_choice = secrets.choice(sign_list)
            if my_choice == their_choice:
                color, icon, resp = 0xFFCC4D, '🔥', 'It\'s a draw'
            elif my_choice == counter:
                color, icon, resp = 0x292929, '💣', 'You lose'
            else:
                color, icon, resp = 0x3B88C3, '💎', 'You win'
            response = discord.Embed(color=color, title=f'{icon} {my_choice.title()}! {resp}!')
        else:
            response = GenericResponse('Invalid sign.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)
