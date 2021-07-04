"""
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

import discord

from sigma.core.utilities.dialogue_controls import DialogueCore
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.minigames.professions.nodes.upgrade_params import upgrade_list
from sigma.modules.minigames.utils.ongoing.ongoing import Ongoing


def get_price_mod(base_price, upgrade_level):
    """
    Gets the level-based price modifier of an upgrade.
    :type base_price: int
    :type upgrade_level:int
    :rtype: int
    """
    return int(base_price * upgrade_level * (1.10 + (0.075 * upgrade_level)))


def get_price(base_price, upgrade_level):
    """
    Gets the total price of an upgrade based on its level.
    :type base_price: int
    :type upgrade_level: int
    :rtype: int
    """
    if upgrade_level == 0:
        upgrade_price = base_price
    else:
        price_mod = get_price_mod(base_price, upgrade_level)
        upgrade_price = price_mod + (price_mod // 2)
    return upgrade_price


async def multi_buy(cmd, pld, choice, level):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type choice: dict
    :type level: int
    """
    currency = cmd.bot.cfg.pref.currency
    user_upgrades = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
    current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
    current_kud = current_kud.current
    upgrade_level = user_upgrades.get(choice.get('id'), 0)
    upgrade_price = 0
    for i in range(1, level + 1):
        upgrade_price += get_price(choice.get("cost"), upgrade_level + i)
    if current_kud >= upgrade_price:
        question = f'Spend {upgrade_price} {currency} on {level} {choice.get("name")} upgrades?'
        question_embed = discord.Embed(color=0xF9F9F9, title=question)
        dialogue = DialogueCore(cmd.bot, pld.msg, question_embed)
        dresp = await dialogue.bool_dialogue()
        if dresp.ok:
            user_upgrades.update({choice.get('id'): upgrade_level + level})
            await cmd.db.set_profile(pld.msg.author.id, 'upgrades', user_upgrades)
            await cmd.db.del_resource(pld.msg.author.id, 'currency', upgrade_price, cmd.name, pld.msg)
            response = GenericResponse(f'Upgraded your {choice.get("name")} to Level {upgrade_level + level}.').ok()
        else:
            response = dresp.generic('upgrade purchase')
    else:
        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
    await pld.msg.channel.send(embed=response)


async def quick_buy(cmd, pld, choice):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type choice: dict
    """
    currency = cmd.bot.cfg.pref.currency
    user_upgrades = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
    upgrade_level = user_upgrades.get(choice.get('id'), 0)
    upgrade_price = get_price(choice.get("cost"), upgrade_level)
    current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
    current_kud = current_kud.current
    if current_kud >= upgrade_price:
        user_upgrades.update({choice.get('id'): upgrade_level + 1})
        await cmd.db.set_profile(pld.msg.author.id, 'upgrades', user_upgrades)
        await cmd.db.del_resource(pld.msg.author.id, 'currency', upgrade_price, cmd.name, pld.msg)
        response = GenericResponse(f'Upgraded your {choice.get("name")} to Level {upgrade_level + 1}.').ok()
    else:
        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
    await pld.msg.channel.send(embed=response)


async def slow_buy(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    currency = cmd.bot.cfg.pref.currency
    if not Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
        Ongoing.set_ongoing(cmd.name, pld.msg.author.id)
        upgrade_file = await cmd.bot.db.get_profile(pld.msg.author.id, 'upgrades') or {}
        upgrade_text = ''
        upgrade_index = 0
        for upgrade in upgrade_list:
            upgrade_index += 1
            upgrade_id = upgrade.get('id')
            upgrade_level = upgrade_file.get(upgrade_id, 0)
            base_price = upgrade.get('cost')
            upgrade_price = get_price(base_price, upgrade_level)
            next_upgrade = upgrade_level + 1
            upgrade_text += f'\n**{upgrade_index}**: Level {next_upgrade} {upgrade["name"]}'
            upgrade_text += f' - {upgrade_price} {currency}'
            upgrade_text += f'\n > {upgrade["desc"]}'
        upgrade_list_embed = discord.Embed(color=0xF9F9F9, title='🛍 Profession Upgrade Shop')
        upgrade_list_embed.description = upgrade_text
        upgrade_list_embed.set_footer(text='Please input the number of the upgrade you want.')
        dialogue = DialogueCore(cmd.bot, pld.msg, upgrade_list_embed)
        dresp = await dialogue.int_dialogue(1, len(upgrade_list))
        if dresp.ok and dresp.value is not None:
            upgrade = upgrade_list[dresp.value - 1]
            current_kud = await cmd.db.get_resource(pld.msg.author.id, 'currency')
            current_kud = current_kud.current
            upgrade_id = upgrade['id']
            upgrade_level = upgrade_file.get(upgrade_id, 0)
            base_price = upgrade['cost']
            upgrade_price = get_price(base_price, upgrade_level)
            if current_kud >= upgrade_price:
                new_upgrade_level = upgrade_level + 1
                upgrade_file.update({upgrade_id: new_upgrade_level})
                await cmd.db.set_profile(pld.msg.author.id, 'upgrades', upgrade_file)
                await cmd.db.del_resource(pld.msg.author.id, 'currency', upgrade_price, cmd.name, pld.msg)
                response = GenericResponse(f'Upgraded your {upgrade["name"]} to Level {new_upgrade_level}.').ok()
            else:
                response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
        else:
            response = discord.Embed(color=0x696969, title='🕙 Sorry, you timed out.')
        if Ongoing.is_ongoing(cmd.name, pld.msg.author.id):
            Ongoing.del_ongoing(cmd.name, pld.msg.author.id)
    else:
        response = GenericResponse('You already have a shop open.').error()
    await pld.msg.channel.send(embed=response)


async def buyupgrade(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    choice = None
    level = None
    if pld.args:
        if len(pld.args) == 2:
            level = pld.args.pop(1)
            if level.isdigit():
                level = abs(int(level))
        try:
            choice = upgrade_list[abs(int(pld.args[0])) - 1]
        except (IndexError, ValueError):
            for upgrade in upgrade_list:
                qry = pld.args[0].lower()
                if upgrade.get('id') == qry:
                    choice = upgrade
                    break
                elif qry in upgrade.get('name').lower() and len(qry) >= 3:
                    choice = upgrade
                    break
    if choice:
        if level and level != 1:
            await multi_buy(cmd, pld, choice, level)
        else:
            await quick_buy(cmd, pld, choice)
    else:
        await slow_buy(cmd, pld)
