command_dict = {}


def command(name):
    """ A decorator that appends a function to the command dictionary defined at the top """
    def _(fn):
        command_dict[name] = fn
    return _


@command("!hi")
async def ping_command(parent, args, user):
    await parent.say("Hello, {0}!".format(user.name))


@command("!quit")
async def quit_command(parent, args, user):
    if parent.is_admin(user):
        await parent.logout()
