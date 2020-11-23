# Delete Discord

**_WARNING_** This script may violate the Discord Terms of Service if used. Your account might be suspended for suspicious activity.

What this does:

It lists all the servers and the channels on your server that your account is a part of. Then, it can delete all of your messages in a server or in a specific channel on a server. This is useful to free up hard disk space on Discord's servers, and so on.

**How to use:**

Python 3.5+ required // https://www.python.org/downloads/

Install discord.py // python3 -m pip install discord.py to install

Run the script.

Enter your username/password that you use to login to discord.

At the menu, you can choose the following:

**1. Select a server**
Provide the name of the server.

**2. Select a channel**
Provide the name of the channel. Must be in a server.

**3. Print a list of all servers this account has joined**
Pretty self-explanatory.

**4. Print a list of all channels on the selected server**
Pretty self-explanatory. A server must be selected with menu option 1.

**5. Delete all messages on the selected server (wow!)**
Delete all messages that your bot wrote on all channels in the selected server. Takes a while!
A server must be selected with menu option 1.

**6. Delete all messages in the selected channel on the selected server"**
Delete all messages that your bot wrote on the selected channels in the selected server. Takes a while as Discord only allows api's to do 2 requests a second and each deleted message is a request! A server must be selected with menu option 1, and a channel must be selected with option 2.

An updated fork of: https://github.com/brian-lui/delete-discord
