import discord
import asyncio

from steam_parser import SteamEventParser
from datetime import datetime

class SpeckChecker(discord.Client):
    def __init__(self, token, channel_id, event_id):
        """ Constructor for the  bot class.

        Args:
            token (str): the token for the discord bot.
            channel_id(str): the id of the channel the bot is going to be working on.
            event_id: the steam id of the group that the bot is going to check the events for.
        """
        super().__init__()

        self.token = token
        self.channel_id = channel_id
        self.channel = discord.Object(id=self.channel_id)

        # Event id for the steam group
        self.event_id =  event_id
        self.event_parser = SteamEventParser(self.event_id)

        # Used for comparing the current event time.
        self.curr_event = datetime.today()
        self.admins = ["superstepa"]

        self._load_commands()

    def get_admins(self):
        ''' A generator that yields all the administrators.'''
        for server in self.servers:
            for member in server.members:
                for role in member.roles:
                    for permission in role.permissions:
                        # permissions are tuples
                        if (permission[0] == "administrator" and
                                permission[1]):
                            yield member

    def is_admin(self, user):
        ''' Checks if a user is an admin '''
        return user in self.get_admins() or user in self.admins

    async def _process_commands(self, message, user):
        # Get the message itself.
        text = message.content

        # Split it into words.
        msg = text.split(' ')

        # The first word is the command.
        command = msg[0]

        # The remainder are the arguments.
        args = msg[1:]

        print("{0} sent: {1} {2}".format(user, command, args))

        for name, func in self.commands.items():
            if (command == name):
                await func(self, args, user)

    async def say(self, message):
        """ Wrapper for send_typing and send_message """
        await self.send_typing(self.channel)
        await self.send_message(self.channel, message)

    def _load_commands(self):
        # command_dict is initialized when commands is imported. It contains all the commands in commands.py
        # Assign all the commands from commands.py to the object.
        from commands import command_dict
        self.commands = command_dict

    def yield_commands(self):
        """Yield all the commands"""
        for command in self.commands:
            yield command

    async def on_message(self, message):
        '''Overloaded Method'''

        # Only process messages if the message is not from the bot itself
        if message.author == self.user:
            return
        await self._process_commands(message, message.author)

    async def on_ready(self):
        '''Overloaded Method'''
        print("Logged in as {0}".format(self.user.name))

    def is_new(self, event):
        """ Checks if the event string dict is newer than current date """
        event_time = "{0} {1}".format(event["Date"], event['Time'])
        event_time = datetime.strptime(event_time, "%A %d %H:%M%p")
        # Add the current day and year to the date
        event_time = event_time.replace(year=datetime.today().year,
                           month=datetime.today().month)
        if (event_time > self.curr_event):
            self.curr_event = event_time
            return True
        else:
            return False

    async def checkEvents(self):
        """ A function that checks if there are any new steam events"""
        await self.wait_until_ready()
        # Piggybacking off this in order to reload all the commands.
        # Ideally this should be in its own method.
        self._load_commands()
        while not self.is_closed:
            try:
                event = self.event_parser.get_last_event()
                if (self.is_new(event)):
                    await self.say("@everyone {0}".format(event["Message"]))
            except Exception as e:
                # Pokemon exception checking. Will hopefully change later.
                pass
            await asyncio.sleep(60)
