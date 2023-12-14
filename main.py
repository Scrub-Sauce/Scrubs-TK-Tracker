#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.1"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"

import os
import discord
from dotenv import load_dotenv
from module.Scoreboard import Scoreboard

# Loads the Discord token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Creates the discord Client
client = discord.Client()

# Creates and loads the scoreboard
scoreboard = Scoreboard()
scoreboard.LoadScoreboard()

# Informs the user when running
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Listens for discord commands
@client.event
async def on_message(message):
    # Creates and executes the +tk command
    if message.content.startswith('+tk'):
        if len(message.mentions) == 2:
            # Parses the Add Date from datetime
            aDate = message.created_at.strftime("%m/%d/%Y")
            userName = "{0}#{1}".format(message.mentions[0].name, message.mentions[0].discriminator)
            scoreboard.newTK(str(message.mentions[0].id), userName, message.mentions[0].display_name,
                             message.mentions[1].display_name, aDate)
            await message.channel.send("{0} just demolished {1}".format(message.mentions[0].mention, message.mentions[1].mention))
        else:
            await message.channel.send("Incorrect Syntax: +tk <@killer> <@victim>\nSee !help for more information")

    # Creates and executes the -tk command
    if message.content.startswith('-tk'):
        if len(message.content.split(' ')) == 4:
            pMessage = message.content.split(' ')
            # Parses the take to be removed from the command line
            rDate = pMessage[3]
            await message.channel.send(scoreboard.removeTK(str(message.mentions[0].id), message.mentions[0].display_name, message.mentions[1].display_name, rDate))
        else:
            await message.channel.send("Incorrect Syntax: -tk <@killer> <@victim> <Date of TK: mm/dd/yyyy>\nSee !help for more information")

    # Creates and executes the !score command
    if message.content.startswith('!score'):
        await message.channel.send("```" + scoreboard.printScore() + "```")

    # Creates and executes the !history command
    if message.content.startswith('!history'):
        if len(message.mentions) == 1:
            await message.channel.send("```" + scoreboard.printUserStats(str(message.mentions[0].id)) + "```")
        else:
            await message.channel.send("Incorrect Syntax: !history <@name>\nSee !help for more information")

    # Creates and executes the !help command
    if message.content.startswith('!help'):
        await message.channel.send("```Commands:"
                                   "\n!help - produces a list of commands"
                                   "\n\n+tk <@killer> <@victim> - requires 2 mentions to function currently you can add any flair you like to the post but keep it at only 2 mentions"
                                   "\n\n-tk <@killer> <@victim> <Date of TK: mm/dd/yyyy> - requires 3 arguements and correct date syntax. Removes TK from players history."
                                   "\n\n!score - produces the team kill record for posts."
                                   "\n\n!history <@name> - produces the users score and history of kills."
                                   "\n\n*NOTE* This bot is very early alpha so please be kind about the bugs. Any suggestions for additions are welcome! DM them to @Scrub Sauce#6207```")

# Runs the discord client
client.run(TOKEN)
