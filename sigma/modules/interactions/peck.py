import discord

from .mech.interaction_mechanics import grab_interaction, get_target, make_footer


async def peck(cmd, message, args):
    interaction = grab_interaction(cmd.db, 'peck')
    target = get_target(message)
    auth = message.author
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0xffcc4d, title=f'😙 {auth.display_name} tries to peck themself.')
    else:
        response = discord.Embed(color=0xffcc4d, title=f'😙 {auth.display_name} pecks {target.display_name}.')
    response.set_image(url=interaction['URL'])
    response.set_footer(text=make_footer(cmd, interaction))
    await message.channel.send(embed=response)
