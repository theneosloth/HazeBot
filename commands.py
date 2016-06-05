command_dict = {}


def command(name):
    """ A decorator that appends a function to the command dictionary defined at the top """
    def _(fn):
        command_dict[name] = fn
    return _


'''

All the commands take three arguments:
parent: discord.Client
args: String of any length.
user: discord.Client

'''

@command("!hi")
async def ping_command(parent, args, user):
    await parent.say("Hello, {0}!".format(user.name))

@command("!help")
async def command_help(parent, args, user):
    message = ""
    for command in parent.yield_commands():
        message+=command
        message+='\n'

    await parent.say(message)

@command("!quit")
async def quit_command(parent, args, user):
    if parent.is_admin(user):
        await parent.say("Good bye")
        await parent.logout()

@command("!coin")
async def coin_command(parent, args, user):
    # Inline import, the module isn't going to be used anywhere else. 
    from random import getrandbits
    await parent.say(['Heads','Tails'][getrandbits(1)])

@command("!roll")
async def roll_command(parent, args, user):
    from random import randrange
    try:
        range = int(args[0])
    except ValueError:
        range = 6
    roll = randrange(1, range)
    await parent.say("Rolled {0} on a {1} sided die.".format(roll, range))
