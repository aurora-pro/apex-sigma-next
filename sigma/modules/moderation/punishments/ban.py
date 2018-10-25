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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar, convert_to_seconds
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import permission_denied
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    log_response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name=f'A User Has Been Banned', icon_url=user_avatar(target))
    log_response.add_field(name='🔨 Banned User',
                           value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_response.add_field(name='🛡 Responsible',
                           value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_response.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_response.set_footer(text=f'user_id: {target.id}')
    return log_response


async def ban(cmd: SigmaCommand, pld: CommandPayload):
    if message.author.permissions_in(message.channel).ban_members:
        if message.mentions:
            target = message.mentions[0]
            timed = args[-1].startswith('--time=')
            try:
                now = arrow.utcnow().timestamp
                endstamp = now + convert_to_seconds(args[-1].split('=')[-1]) if timed else None
            except (LookupError, ValueError):
                err_response = discord.Embed(color=0xBE1931, title='❗ Please use the format HH:MM:SS.')
                await message.channel.send(embed=err_response)
                return
            if len(args) >= 2:
                try:
                    if endstamp:
                        clean_days = int(args[-2])
                    else:
                        clean_days = int(args[-1])
                except ValueError:
                    clean_days = 0
            else:
                clean_days = 0
            clean_days = clean_days if clean_days in [0, 1, 7] else 0
            if cmd.bot.user.id != target.id:
                if message.author.id != target.id:
                    above_hier = hierarchy_permit(message.author, target)
                    is_admin = message.author.permissions_in(message.channel).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(message.guild.me, target)
                        if above_me:
                            rarg = args[1:-1] if timed else args[1:] if args[1:] else None
                            reason = ' '.join(rarg) if rarg else None
                            response = discord.Embed(color=0x696969, title=f'🔨 The user has been banned.')
                            response_title = f'{target.name}#{target.discriminator}'
                            response.set_author(name=response_title, icon_url=user_avatar(target))
                            to_target = discord.Embed(color=0x696969)
                            to_target.add_field(name='🔨 You have been banned.', value=f'Reason: {reason}')
                            to_target.set_footer(text=f'From: {message.guild.name}.', icon_url=message.guild.icon_url)
                            try:
                                await target.send(embed=to_target)
                            except discord.Forbidden:
                                pass
                            audit_reason = f'By {message.author.name}: {reason}'
                            await target.ban(reason=audit_reason, delete_message_days=clean_days)
                            log_embed = generate_log_embed(message, target, reason)
                            await log_event(cmd.bot, message.guild, cmd.db, log_embed, 'log_bans')
                            if endstamp:
                                doc_data = {'server_id': message.guild.id, 'user_id': target.id, 'time': endstamp}
                                await cmd.db[cmd.db.db_nam].BanClockworkDocs.insert_one(doc_data)
                        else:
                            response = discord.Embed(color=0xBE1931, title='⛔ Target is above my highest role.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ Can\'t ban someone equal or above you.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You can\'t ban yourself.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t ban myself.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = permission_denied('Ban permissions')
    await message.channel.send(embed=response)
