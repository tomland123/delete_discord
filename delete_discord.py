"""
WARNING: Use for bot accounts only! Using this for user (human) accounts is a
serious Discord TOS violation.

This script deletes your Discord bot account's messages from specified servers
and/or channels. Requires discord.py.

Usage:

Run delete_discord.py

Enter your username/password that you use to login to discord.

At the menu, you can choose the following:
"1. Select a server"
Provide the name of the server (not the ID). You can get a list of servers by
using menu option 3.

"2. Select a channel"
Provide the index of the channel (not the name). You can get a list of channels
by using menu option 4.

"3. Print a list of all servers this account has joined"
Pretty self-explanatory.

"4. Print a list of all channels on the selected server"
Pretty self-explanatory. A server must be selected with menu option 1.

"5. Delete all messages on the selected server"
Delete all messages that your bot wrote on all channels in the selected server.
Takes a while! A server must be selected with menu option 1.

"6. Delete all messages in the selected channel on the selected server"
Delete all messages that your bot wrote on the selected channels in the
selected server. Takes a while! A server must be selected with menu option 1,
and a channel must be selected with option 2.

"7. Quit"
Quit.
"""

import asyncio
import discord


class ClientManager():
    """ Handles the user input and sends it to the Discord servers.
    Event loop for user input is handled in menu_loop. Each time an operation
    is selected that needs to communicate with the server, the following steps
    are performed in run_coroutine:
            1. Create a new async event loop
            2. Initialize a new Discord client object
            3. Add the requested coroutine to the queue
            4. Login, run the coroutine as the only operation, logout

    Look if you're so good at coding you can make a better workflow that
    doesn't involve logging in and out for every operation, ok?
    """

    def __init__(self):
        self.client = None
        self.quit_now = False
        self.selected_server = None
        self.selected_channel = -1

    # coroutines here
    async def get_servers_coro(self):
        print("Getting server list from Discord, please be patient...")
        await self.client.wait_until_ready()
        servers = self.client.guilds
        return servers

    async def print_servers_coro(self):
        servers = await self.get_servers_coro()
        for server in servers:
            print(server.id, server.name)
        await self.client.logout()

    async def get_channels_coro(self):
        servers = await self.get_servers_coro()
        try:
            server = [server for server in servers if server.name ==
                      self.selected_server][0]
            channels = server.channels

            return list(channels)
        except IndexError:
            print("No server with that name found")
            return None

    async def print_channels_coro(self):
        unfilteredChannels = await self.get_channels_coro()
        channels = list(
            filter(lambda x: isinstance(x, discord.TextChannel), unfilteredChannels))
        if channels:
            for i in range(len(channels)):
                print(str(i) + ": " + channels[i].name)
        else:
            print("Not listing channels because the channel couldn't be retrieved")
        await self.client.logout()

    async def delete_server_coro(self):
        channels = await self.get_channels_coro()
        if not channels:
            print("Server with this name not found")
            await self.client.logout()
            return

        response = input("Delete ALL messages from " + self.selected_server +
                         "? Type YES (all caps and then press enter) to confirm: ")
        if response != "YES":
            print("We didn't get the go-ahead so we aren't deleting everything")
            await self.client.logout()
            return

        channels = await self.get_channels_coro()
        count = 0
        if channels:
            for i in range(len(channels)):
                print(channels[i])
                if(isinstance(channels[i], discord.TextChannel)):
                    async for m in channels[i].history(limit=10000000):
                        if (m.author == self.client.user):
                            count += 1
                            await m.delete()
                        if count > 0 and count % 100 == 0:
                            print(str(count) + " messages deleted so far...")
            print("Deleted " + str(count) +
                  " messages from channel " + channels[i].name)
        else:
            print("Not listing channels because the channel couldn't be retrieved")
        await self.client.logout()

    async def delete_channel_coro(self, called_from_server_delete=None):
        count = 0
        channels = await self.get_channels_coro()

        if not isinstance(self.selected_channel, str):
            print("Please enter a channel to delete")
            await self.client.logout()
            return

        if not channels:
            print("Server with this name not found")
            await self.client.logout()
            return

        if called_from_server_delete is None:
            response = input("Delete all messages in " +
                             self.selected_channel + "? Type YES (enter) to confirm: ")
            if response != "YES":
                print("We didn't get the go-ahead so we aren't deleting everything")
                await self.client.logout()
                return
        try:
            if channels:
                for i in range(len(channels)):
                    if(channels[i].name == self.selected_channel):
                        async for m in channels[i].history(limit=10000000):
                            if (m.author == self.client.user):
                                count += 1
                                await m.delete()
                            if count > 0 and count % 100 == 0:
                                print(str(count) + " messages deleted so far...")
            print("Deleted " + str(count) +
                  " messages from channel " + self.selected_channel)
            await self.client.logout()

        except ValueError:
            print(ValueError, "Didn't manage to successfully delete from " +
                  self.selected_channel, self.client.user)
            return self.selected_channel

        # if called_from_server_delete is None:
        # 	await self.client.logout()

    def run_coroutine(self, coro):
        """ This function gets stuff from the discord. It logs in and logs out
        for each operation because I can't figure out how to pass control back
        without logging out lol. I only know so much :confounded:
        Uh anyway, this function accepts an async function with no arguments
        """

        asyncio.set_event_loop(asyncio.new_event_loop())
        self.client = discord.Client()
        self.client.loop.create_task(coro())
        self.client.run(self.token, bot=False)

    # These functions pass the coroutines to self.run_coroutine
    def print_servers(self):
        self.run_coroutine(self.print_servers_coro)

    def menu_select_server(self):
        self.run_coroutine(self.menu_select_server_coro)

    def menu_select_channel(self):
        self.run_coroutine(self.menu_select_channel_coro)

    def print_channels(self):
        self.run_coroutine(self.print_channels_coro)

    def delete_server_messages(self):
        self.run_coroutine(self.delete_server_coro)

    def delete_channel_messages(self):
        self.run_coroutine(self.delete_channel_coro)

    # menu here

    def menu_quit(self):
        self.quit_now = True

    async def menu_select_server_coro(self):
        servers = await self.get_servers_coro()
        for server in servers:
            print(server.id, server.name)

        response = input(
            "Which server do you want to select? Please enter the server's NAME: ")
        # if you have two servers with the same name I can't help you sorry
        self.selected_server = response
        print("\nServer name has been set to: " + response)
        await self.client.logout()

    async def menu_select_channel_coro(self):
        unfilteredChannels = await self.get_channels_coro()
        channels = list(
            filter(lambda x: isinstance(x, discord.TextChannel), unfilteredChannels))

        if channels:
            for i in range(len(channels)):
                print(str(i) + ": " + channels[i].name)

        response = input(
            "Which channel do you want to select? Please enter the channel's NAME: ")
        try:
            self.selected_channel = response
            print("\nChannel name has been set to: " + response)
            await self.client.logout()
        except:
            print("\nDidn't get a number. Please enter a number, not the channel name.")

    def menu_main(self):
        response = input(
            "\nLet's delete our discord history!\n\n"
            "1. Select a server\n"
            "2. Select a channel\n"
            "3. Print a list of all servers this account has joined\n"
            "4. Print a list of all channels on the selected server\n"
            "5. Delete all messages on the selected server (wow!)\n"
            "6. Delete all messages in the selected channel on the selected server\n"
            "7. Quit\n\n"

            "Currently selected server: %s\n"
            "Currently selected channel: %s\n\n"

            "Just type in the number and press enter\n"
            % (self.selected_server, self.selected_channel)
        )

        funcs = {
            "1": self.menu_select_server,
            "2": self.menu_select_channel,
            "3": self.print_servers,
            "4": self.print_channels,
            "5": self.delete_server_messages,
            "6": self.delete_channel_messages,
            "7": self.menu_quit,
        }

        try:
            return funcs[response]
        except KeyError:
            print("Hey sorry that wasn't a correct choice can you try again")
            return None
        except:
            print("Holy crap how did you get here. Please post an issue")

    def menu_loop(self):
        while not self.quit_now:
            func = self.menu_main()
            if func:
                func()

    def menu_credentials(self):
        # If you wanna submit a pull request to improve this section please do
        print("Don't run this on a public computer. Not sure what a token is? Checkout this website:")
        self.token = input("Enter your discord token: ")


dog = ClientManager()
dog.menu_credentials()
dog.menu_loop()
