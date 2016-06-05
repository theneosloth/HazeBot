import discord
import asyncio

from steam_parser import SteamEventParser
from datetime import datetime
from commands import command_dict


class SpeckChecker(discord.Client):
    def __init__(self, token, channel_id, event_id):
        super().__init__()

        self.token = token
        self.channel_id = channel_id
        self.channel = discord.Object(id=self.channel_id)

        # Event id for the steam group
        self.event_id =  event_id
        self.event_parser = SteamEventParser(self.event_id)

        # Used for comparing the current event time.
        self.curr_event = datetime.now()
        self.commands = command_dict

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
        return user in self.get_admins()

    async def process_commands(self, message, user):
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
        ''' Wrapper for send_typing and send_message '''
        await self.send_typing(self.channel)
        await self.send_message(self.channel, message)

    async def on_message(self, message):
        '''Overloaded Method'''

        # Only process messages if the message is not from the bot itself
        if message.author == self.user:
            return
        await self.process_commands(message, message.author)

    async def on_ready(self):
        '''Overloaded Method'''
        print("Logged in as {0}".format(self.user.name))
        await self.say("Hello World")

    def is_new(self, event):
        ''' Checks if the event string dict is newer than current date '''
        event_time = "{0} {1}".format(event["Date"], event['Time'])
        event_time = datetime.strptime(event_time, "%A %d %H:%M%p")
        event_time.replace(year=datetime.today().year)
        if (event_time > self.curr_event):
            self.curr_event = event_time
            return True
        else:
            return False

    async def checkEvents(self):
        ''' A function that checks if there are any new steam events'''
        await self.wait_until_ready()
        while not self.is_closed:
            event = self.event_parser.get_last_event()
            if (self.is_new(event)):
                await self.say(event["Message"])
            await asyncio.sleep(60)

