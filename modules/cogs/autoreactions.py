from modules.functions.helpers import *
from modules.functions.checkers import *

"""

#----------------------------------------------------------------
# Autoreact command

@client.command(aliases=["ar"])
@commands.check_any(commands.is_owner(), check_whitelist())
async def autoreact(ctx, member : discord.Member, *, reaction):

    print(type(reaction))
    reaction = f'\\u{ord(str(reaction)):08x}'

    if False and "\\u" not in reaction:
        await ctx.send(':warning: **Invalid arguments. Make sure yousend the actual emoji, not the string (`:duck:`, not `duck`).\nUsage:**  `n!autoreact <username> <emote>`')
        debug_print('[Bot] Could not parse arguments (Invalid emoji %s) for user: %s' % (reaction, ctx.author))
        return

    bak_config_file(config_path)
    with open(config_path, "r") as ifile:
        json_data = json.loads(ifile.read())

    if ctx.guild.id in json_data['autoreact_list']:
        if member.id in json_data['autoreact_list'][ctx.guild.id]:
            if str(reaction) not in json_data['autoreact_list'][str(ctx.guild.id)][str(member.id)]:
                # append reaction
                json_data['autoreact_list'][str(ctx.guild.id)][str(member.id)].append(reaction)
                debug_print('[Bot] User %s added autoreaction (%s) for user %s.' % (ctx.author, reaction, member.display_name))
            else:
                debug_print('[Bot] User %s tried to add autoreactions for user %s but it was in the json.' % (ctx.author, member.display_name))
        else:
            # append user and reaction
            json_data['autoreact_list'][str(ctx.guild.id)].update({str(member.id): []})
            json_data['autoreact_list'][str(ctx.guild.id)][str(member.id)].append(reaction)
            debug_print('[Bot] User %s added autoreaction (%s) for user %s.' % (ctx.author, reaction, member.display_name))
    else:
        # add guild, user and reaction
        json_data['autoreact_list'].update({str(ctx.guild.id): {}})
        json_data['autoreact_list'][str(ctx.guild.id)].update({str(member.id): []})
        json_data['autoreact_list'][str(ctx.guild.id)][str(member.id)].append(reaction)
        debug_print('[Bot] User %s added autoreaction (%s) for user %s.' % (ctx.author, reaction, member.display_name))

    with open(config_path, "w") as ofile:
        ofile.write(json.dumps(json_data, indent=4))


    embed = discord.Embed(title="Done", description="**%s** added autoreactions to **%s**" % (ctx.author.display_name, member.display_name), color=0x11ff11)
    await ctx.send(embed=embed)

@autoreact.error
async def autoreact_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':warning: **Missing required arguments. Usage:**  `n!autoreact <username> <emote_str>`')
        debug_print('[Bot] Could not parse arguments (Not enough arguments) for user: %s' % ctx.author)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(':warning: **Member not found. Make sure you don\'t use nicknames.**')
        debug_print('[Bot] Could not parse arguments (No member) for user: %s' % ctx.author)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: **You don\'t have the permissions to do that, %s.**' % ctx.author.mention)
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
    else:
        await ctx.send(':warning: **Unknown error. Contact the bot owner.**')
        debug_print('[Bot] Could not parse arguments for user: %s' % ctx.author)
        error_print(error)

"""
