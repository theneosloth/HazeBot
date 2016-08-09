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
    """Says hi back"""
    await parent.say("Hello, {0}!".format(user.name))

@command("!help")
async def command_help(parent, args, user):
    """Lists all the commands the bot has"""
    message = ""
    for command in parent.yield_commands():
        message+=command
        message+='\n'

    await parent.say(message)

@command("!quit")
async def quit_command(parent, args, user):
    """Shuts down. Only admins can use this"""
    if parent.is_admin(user):
        print("Logged out as {0}".format(parent.user.name))
        await parent.logout()

@command("!coin")
async def coin_command(parent, args, user):
    """Flips a coin"""
    # Inline import, the module isn't going to be used anywhere else.
    from random import getrandbits
    await parent.say(['Heads','Tails'][getrandbits(1)])

@command("!roll")
async def roll_command(parent, args, user):
    """Rolls an X sided dice. 6 is the default"""
    from random import randrange
    # Clunky, temporary (and therefore permanent) solution.
    if (len(args) < 1):
        range = 6
    else:
        try:
            range = int(args[0])
        except (ValueError, KeyError):
            range = 6
    roll = randrange(1, range)
    await parent.say("Rolled {0} on a {1} sided die.".format(roll, range))

@command("!game")
async def command_game(parent, args, user):
    """Loads help for a game from a help.json file"""

    from json import loads
    import os

    ERROR_MSG = "Invalid format, expected format is: \"!help UT99/UT2004/JA \"."
    ERROR_MSG += "\nFor connection info use !help UT99/UT2004/JA connect"
    if (len(args) < 1):
        await parent.say(ERROR_MSG)
        return

    FILE_NAME = "../data/help.json"
    path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    default_request = "general"

    try:
        game = args[0].lower()
        request = args[1].lower()
    except IndexError:
        request = default_request

    with open(path, 'r') as f:
        data = loads(f.read())
        try:
            msg = "\n".join(data[game][request])
        except KeyError:
            msg = ERROR_MSG
        await parent.say(msg)

@command("!choice")
async def choice_command(parent, args, user):
    """Resolves an argument"""
    from random import choice
    # Removes all 'or' from arguments
    await parent.say("I choose: {0}".format(
        choice([x for x in args if x != "or"])))

@command("!event")
async def event_command(parent, args, user):
    """Prints the last time Speck hosted a game"""
    event = parent.get_last_event()
    await parent.say("{0} @ {1}, {2}".format(
        event["Message"], event["Date"], event["Time"]))

@command("!nuke")
async def nuke_command(parent, args, user):
    """Deletes all the messages from a passed channel"""
    if (len(args) == 0):
        await parent.say("Please pass a channel name after '!nuke'")
        return

    if parent.is_admin(user):
        for server in parent.servers:
            for channel in server.channels:
                for arg in args:
                    if (channel.name == arg):
                        deleted = await parent.purge_from(
                            channel,
                            check = lambda m: True)
