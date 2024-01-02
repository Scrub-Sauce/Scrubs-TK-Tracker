#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.2"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"

import os
import discord
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

# Loads the Discord token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = conn.cursor()

# Creates the discord Client
bot = commands.Bot(command_prefix='/', intents=intents)


# Informs the user when running
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


#                                    "\n!help - produces a list of commands"
#                                    "\n\n+tk <@killer> <@victim> - requires 2 mentions to function currently you can add any flair you like to the post but keep it at only 2 mentions"
#                                    "\n\n-tk <@killer> <@victim> <Date of TK: mm/dd/yyyy> - requires 3 arguements and correct date syntax. Removes TK from players history."
#                                    "\n\n!score - produces the team kill record for posts."
#                                    "\n\n!history <@name> - produces the users score and history of kills."
#                                    "\n\n*NOTE* This bot is very early alpha so please be kind about the bugs. Any suggestions for additions are welcome! DM them to @Scrub Sauce#6207```")


# @bot.command()
# async def test(ctx, user: discord.Member):


@bot.command()
async def tk(ctx, killer: discord.Member, victim: discord.Member):
    tk_messages = [
        f'{killer} delivers a surprise performance, starring {victim} as the unexpected guest star.',
        f'{killer} and {victim} - redefining teamwork, one unexpected kill at a time.',
        f'In the game of life, {killer} just played the "unintentional takedown" card on {victim}.',
        f'Friendly fire: the secret weapon of {killer}\'s strategic masterplan against {victim}.',
        f'{killer} and {victim} - proving that teamwork makes the dream work, even if it\'s a nightmare.',
        f'Congratulations, {killer}! You just earned the "Worst Wingman" award by taking down {victim}.',
        f'Is it a bird? Is it a plane? No, it\'s just {killer} unintentionally wrecking {victim}\'s day.',
        f'{killer} takes the lead in the "Oops, I Did It Again" competition with {victim} as a reluctant co-star.',
        f'Who needs enemies when you have allies like {killer}? Poor {victim}.',
        f'{killer} just proved that when in doubt, shoot everything. Including {victim}. Don\'t forget to check his body for snacks!',
        f'Warning: {killer} may cause sudden drops in team morale by taking out {victim} at the worst times.',
        f'Did {killer} just perform a magic trick? Poof! {victim} disappears in a cloud of bullets.',
        f'Friendly fire: {killer}\'s unique strategy to keep {victim} on their toes.',
        f'In the grand saga of {killer} versus {victim}, today\'s chapter ends with an unexpected twist.',
        f'Brace yourselves for the {killer} and {victim} show - where every kill is an accidental masterpiece.',
        f'Hold onto your hats, folks! {killer} just turned {victim} into an unintentional food critic with only lead on the menu.',
        f'Move over, strategists! {killer} just introduced the revolutionary "unintentional flanking" technique on {victim}.',
        f'{killer} just demonstrated to {victim} why warning labels exist.',
        f'{killer} and {victim} - the pioneers of tactical chaos, bringing a whole new meaning to "friendly" competition.',
        f'{killer} and {victim} - proving that sometimes the best strategy is no strategy at all.',
        f'{victim}, pleading won\'t save you. {killer} REALLY enjoys Flux Pavilion... "I CANT STOP, OP, OP..."',
        f'Presenting the {killer} and {victim} circus - where every match is a tightrope walk of accidental takedowns.',
        f'Is it strategy or is it chaos? {killer} blurs the lines with {victim} caught in the crossfire.',
        f'In the world of accidental eliminations, {killer} channels their inner Private Pile on {victim}',
        f'{killer} gave {victim} a warriors death.',
        f'{killer}, you killed {victim}! Oh my god, you bastard!',
        f'{killer} ait {victim}\'s lunch.',
        f'{killer} had a Nam flashback and {victim} looked like the charlie.',
        f'{victim} decided to play jody, and {killer} found out.',
        f'{killer} just bulldozed {victim} in true Jibby fashion. He would be so proud.',
        f'{killer} gave {victim} the Old Yeller treatment.'
    ]
    kill_datetime = datetime.now()
    kill_date = kill_datetime.strftime("%m/%d/%Y")
    kill_time = kill_datetime.strftime("%H:%M")
    await ctx.send(
        f'Name: {killer.name} \nDisplay Name: {killer.display_name} \nDiscriminator: {killer.discriminator} \nID: {killer.id}')


@bot.command()
async def server(ctx):
    server_id = ctx.guild.id
    await ctx.send(f'Server ID: {server_id}')


# async def tk_remove(ctx, killer, victim, date):
#
# async def score(ctx):
#
# async def history(ctx):


# Runs the discord client
bot.run(TOKEN)
