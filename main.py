#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.2"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"

import os
import discord
import random
from controller.DB_Manager import *
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

# Loads the Discord token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Creates the discord Client
bot = commands.Bot(command_prefix='$', intents=intents,help_command=None)


# Informs the user when running
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def test(ctx):
    records = fetch_user(123456)
    print(records)
    await ctx.send(f'{records}')
@bot.command()
async def help(ctx):
    await ctx.send('Available commands: ```/help - List all commands\n/tk <@killer> <@victim> - Adds a TK to the tracker.\n/tk_remove\n/score - Produces the teamkill scoreboard.\n/history <@killer> - Produces a history of player\'s teamkills.\n/info - Provides information on the author.```')

@bot.command()
async def tk(ctx, killer: discord.Member, victim: discord.Member):
    tk_messages = [
        f'{killer.mention} delivers a surprise performance, starring {victim.mention} as the unexpected guest star. The act for the night: Death by firing squad.',
        f'{killer.mention} and {victim.mention} - redefining teamwork, one unexpected kill at a time.',
        f'In the game of life, {killer.mention} just played the "unintentional takedown" card on {victim.mention}.',
        f'Friendly fire: the secret weapon of {killer.mention}\'s strategic masterplan against {victim.mention}.',
        f'{killer.mention} and {victim.mention} - proving that teamwork makes the dream work, even if it\'s a nightmare.',
        f'Congratulations, {killer.mention}! You just earned the "Worst Wingman" award by taking down {victim.mention}.',
        f'Is it a bird? Is it a plane? No, it\'s just {killer.mention} unintentionally wrecking {victim.mention}\'s day.',
        f'{killer.mention} takes the lead in the "Oops, I Did It Again" competition with {victim.mention} as a reluctant co-star.',
        f'Who needs enemies when you have allies like {killer.mention}? Poor {victim.mention}.',
        f'{killer.mention} just proved that when in doubt, shoot everything. Including {victim.mention}. Don\'t forget to check his body for snacks!',
        f'Warning: {killer.mention} may cause sudden drops in team morale by taking out {victim.mention} at the worst times.',
        f'Did {killer.mention} just perform a magic trick? Poof! {victim.mention} disappears in a cloud of bullets.',
        f'Friendly fire: {killer.mention}\'s unique strategy to keep {victim.mention} on their toes.',
        f'In the grand saga of {killer.mention} versus {victim.mention}, today\'s chapter ends with an unexpected twist.',
        f'Brace yourselves for the {killer.mention} and {victim.mention} show - where every kill is an accidental masterpiece.',
        f'Hold onto your hats, folks! {killer.mention} just turned {victim.mention} into an unintentional food critic with only lead on the menu.',
        f'Move over, strategists! {killer.mention} just introduced the revolutionary "unintentional flanking" technique on {victim.mention}.',
        f'{killer.mention} just demonstrated to {victim.mention} why warning labels exist.',
        f'{killer.mention} and {victim.mention} - the pioneers of tactical chaos, bringing a whole new meaning to "friendly" competition.',
        f'{killer.mention} and {victim.mention} - proving that sometimes the best strategy is no strategy at all.',
        f'{victim.mention}, pleading won\'t save you. {killer.mention} REALLY enjoys Flux Pavilion... "I CANT STOP, OP, OP..."',
        f'Presenting the {killer.mention} and {victim.mention} circus - where every match is a tightrope walk of accidental takedowns.',
        f'Is it strategy or is it chaos? {killer.mention} blurs the lines with {victim.mention} caught in the crossfire.',
        f'In the world of accidental eliminations, {killer.mention} channels their inner Private Pile on {victim.mention}',
        f'{killer.mention} gave {victim.mention} a warriors death.',
        f'{killer.mention}, you killed {victim.mention}! Oh my god, you bastard!',
        f'{killer.mention} ait {victim.mention}\'s lunch.',
        f'{killer.mention} had a Nam flashback and {victim.mention} looked like the charlie.',
        f'{victim.mention} decided to play jody, and {killer.mention} found out.',
        f'{killer.mention} just bulldozed {victim.mention} in true Jibby fashion. He would be so proud.',
        f'{killer.mention} gave {victim.mention} the Old Yeller treatment.'
    ]

    rng = random.randint(0, (len(tk_messages) - 1))
    status_add_kill = add_teamkill(killer, victim, ctx.guild)

    if status_add_kill:
        await ctx.send(tk_messages[rng])
    else:
        await ctx.send(f"There was an error adding the TK please contact the TK Bot Administrator.")


# async def tk_remove(ctx, killer, victim, kill_id):
#
# async def score(ctx):
#
# async def history(ctx):


# Runs the discord client
bot.run(TOKEN)
