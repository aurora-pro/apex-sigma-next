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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


async def dadjoke(cmd: SigmaCommand, pld: CommandPayload):
    joke_list = await cmd.db[cmd.db.db_nam].DadjokeData.find().to_list(None)
    end_joke_choice = secrets.choice(joke_list)
    end_joke = end_joke_choice.get('setup')
    punchline = end_joke_choice.get('punchline')
    response = discord.Embed(color=0xFFDC5D)
    response.add_field(name='😖 Have An Awful Dad Joke', value=f'{end_joke}... {punchline}')
    await message.channel.send(embed=response)
