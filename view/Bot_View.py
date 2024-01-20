import os
import discord
import random
from discord.ext.commands import bot
from controller.Bot_Controller import *
from model.Teamkill import Teamkill
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle


def run_bot():
    intents = discord.Intents.all()

    # Loads the Discord token from .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Creates the discord Client
    bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

    # Informs the user when running
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f'{bot.user} has connected to Discord!')

    @bot.tree.command(name='history', description='Displays the kill log for the mentioned player.')
    async def history(req_obj: discord.Interaction, killer: discord.Member):
        h_status, h_data = get_kill_history(killer)
        if h_status:
            card = discord.Embed(title=f'{killer.display_name} Team Kill History',
                                 description=f'The following is the log of all past team kills by {killer.display_name}',
                                 color=discord.Color.random())
            card.add_field(name='Killer', value=f'<@{killer.id}>', inline=True)
            card.add_field(name='Kill Count', value=f'{h_data[0]}', inline=True)
            kill_data = h_data[1]
            for line in kill_data:
                kill_id = line[0]
                victim_id = line[1]
                kill_occur = line[2].strftime("%m/%d/%y @ %I:%M %p")
                kill_note = line[3]
                if kill_note is not None:
                    card.add_field(name="",
                                   value=f'**ID:** {kill_id} - <@{victim_id}> - {kill_occur} - **Note:** {kill_note}',
                                   inline=True)
                else:
                    card.add_field(name="", value=f'**ID:** {kill_id} - <@{victim_id}> - {kill_occur}',
                                   inline=False)
            await req_obj.response.send_message(embed=card)

    @history.error
    async def history_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='help',
                      description='Displays all available commands and the context in which they can be used.')
    async def help(req_obj: discord.Interaction):
        card = discord.Embed(title="Help", description="Here are all available commands and how they can be used.",
                             color=discord.Colour.random())
        card.add_field(name="Add Team kill", value="`/tk` `<@Killer>` `<@Victim>` - Adds a teamkill to the tracker",
                       inline=False)
        card.add_field(name="Leaderboard Top 15",
                       value="`/top15` - Displays a table of the top 15 team killers on this discord server.",
                       inline=False)
        card.add_field(name="History", value="`/hisroty` `<@Killer>` - Displays the kill log for the mentioned player.",
                       inline=False)
        card.add_field(name="Remove Team kill",
                       value="`/tk` `<Kill ID>` - Removes the specified team kill from the bot. Requires 'Move Member' permissions.",
                       inline=False)
        card.add_field(name="Wipe Tracker",
                       value="`/wipe_bot` `<Are You Sure>` - Wipes the team kill tracker of all logged kills. Requires 'Adminstrator' permisions. are_you_sure must be 'Yes' to confirm.",
                       inline=False)
        card.add_field(name="Help",
                       value="`/help` Displays all available commands and the context in which they can be used. You just used it...",
                       inline=False)
        await req_obj.response.send_message(embed=card)

    @help.error
    async def help_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='wipe_bot',
                      description='Wipes the team kill tracker of all logged kills. Requires Admin Permision. are_you_sure = yes')
    @app_commands.checks.has_permissions(administrator=True)
    async def wipe_bot(req_obj: discord.Interaction, are_you_sure: str):
        if are_you_sure.upper() == 'YES':
            wipe_status = wipe_server_tks(req_obj.guild)
            if wipe_status:
                await req_obj.response.send_message(f'{req_obj.guild.name} Team kills have been sucessfully wiped.')
            else:
                await req_obj.response.send_message(f'There was an error wiping {req_obj.guild.name} Team kills.')

        else:
            await req_obj.response.send_message('Aborting bot wipe...')

    @wipe_bot.error
    async def wipe_bot_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='top15', description='Displays the a leaderboard of the top 15 team killers')
    async def top15(req_obj: discord.Interaction):
        lb_status, lb_data = get_leaderboard_data(req_obj.guild)
        if lb_status:
            card = discord.Embed(title=f'{req_obj.guild.name} - Top 15 Team Killers',
                                 description='Here are your biggest shitters', color=discord.Colour.random())
            for i in range(0, len(lb_data)):
                card.add_field(name='', value=f'{i + 1}. <@{lb_data[i][0]}> - Kill Count: {lb_data[i][1]}',
                               inline=False)
            await req_obj.response.send_message(embed=card)
        else:
            await req_obj.response.send_message(f"Unable to display leaderboard at this time.")

    @top15.error
    async def top15_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name="tk", description="Adds a teamkill to the tracker")
    async def tk(req_obj: discord.Interaction, killer: discord.Member, victim: discord.Member, note: str = None):
        tk_messages = [
            [
                f'{killer.mention} delivers a surprise performance, starring {victim.mention} as the unexpected guest star. The act for the night: Death by firing squad.',
                "https://media1.tenor.com/m/tYguIlmfrcoAAAAC/surprise-gifkaro.gif"],
            [f'{killer.mention} and {victim.mention} - redefining teamwork, one unexpected kill at a time.',
             "https://media1.tenor.com/m/4Puijom5EmAAAAAC/trust-fail-fall.gif"],
            [
                f'In the game of life, {killer.mention} just played the "unintentional takedown" card on {victim.mention}.',
                "https://media1.tenor.com/m/KVwKOENJzpQAAAAd/fedor-emelianenko-kevin-randleman.gif"],
            [f'Friendly fire: the secret weapon of {killer.mention}\'s strategic masterplan against {victim.mention}.',
             "https://media1.tenor.com/m/uUV4KxpD7jcAAAAd/plan-conspiracy.gif"],
            [
                f'{killer.mention} and {victim.mention} - proving that teamwork makes the dream work, even if it\'s a nightmare.',
                "https://media1.tenor.com/m/k0e1MR9Ra8IAAAAd/survivor-rowing.gif"],
            [
                f'Congratulations, {killer.mention}! You just earned the "Worst Wingman" award by taking down {victim.mention}.',
                "https://media1.tenor.com/m/ViRu1oYgODMAAAAC/south-park-cartman.gif"],
            [
                f'Is it a bird? Is it a plane? No, it\'s just {killer.mention} unintentionally wrecking {victim.mention}\'s day.',
                "https://media1.tenor.com/m/Bm87ctQSQBEAAAAC/birb-fly.gif"],
            [
                f'{killer.mention} takes the lead in the "Oops, I Did It Again" competition with {victim.mention} as a reluctant co-star.',
                "https://media1.tenor.com/m/OoFDdPceaQEAAAAd/oops-i-did-it-again.gif"],
            [f'Who needs enemies when you have allies like {killer.mention}? Poor {victim.mention}.',
             "https://media1.tenor.com/m/U7gBj-PISdgAAAAd/jump-fail-prank.gif"],
            [
                f'{killer.mention} just proved that when in doubt, shoot everything. Including {victim.mention}. Don\'t forget to check his body for snacks!',
                "https://media1.tenor.com/m/9mjeGBGkFZYAAAAC/guns-shooting.gif"],
            [
                f'Warning: {killer.mention} may cause sudden drops in team morale by taking out {victim.mention} at the worst times.',
                "https://media1.tenor.com/m/o-kpBv0RkcEAAAAC/soul-in-danger.gif"],
            [
                f'Did {killer.mention} just perform a magic trick? Poof! {victim.mention} disappears in a cloud of bullets.',
                "https://media1.tenor.com/m/TikTdDzl4zAAAAAC/magic-confetti.gif"],
            [f'Friendly fire: {killer.mention}\'s unique strategy to keep {victim.mention} on their toes.',
             "https://media1.tenor.com/m/beImWqThNaMAAAAd/gun-shooting.gif"],
            [
                f'In the grand saga of {killer.mention} versus {victim.mention}, today\'s chapter ends with an unexpected twist.',
                "https://media1.tenor.com/m/JBmnjSa2LJkAAAAC/plot-twist.gif"],
            [
                f'Brace yourselves for the {killer.mention} and {victim.mention} show - where every kill is an accidental masterpiece.',
                "https://media1.tenor.com/m/ASZh9wrkwv0AAAAC/aleph-zero-alephzero.gif"],
            [
                f'Hold onto your hats, folks! {killer.mention} just turned {victim.mention} into an unintentional food critic with only lead on the menu.',
                "https://media1.tenor.com/m/mXxNnrR5n4QAAAAd/good-great.gif"],
            [
                f'Move over, strategists! {killer.mention} just introduced the revolutionary "unintentional flanking" technique on {victim.mention}.',
                "https://media1.tenor.com/m/v6jejtzA8HAAAAAC/we-attack-their-weak-spot-eric-cartman.gif"],
            [f'{killer.mention} just demonstrated to {victim.mention} why warning labels exist.',
             "https://media1.tenor.com/m/Z0bIoPRxc2gAAAAC/fall-trip.gif"],
            [
                f'{killer.mention} and {victim.mention} - the pioneers of tactical chaos, bringing a whole new meaning to "friendly" competition.',
                "https://media1.tenor.com/m/TX8jMsh0EfAAAAAC/buggy-horse-and-buggy.gif"],
            [f'{killer.mention} and {victim.mention} - proving that sometimes the best strategy is no strategy at all.',
             "https://media.tenor.com/evpSQei_eb4AAAAM/plan-star-lord.gif"],
            [
                f'{victim.mention}, pleading won\'t save you. {killer.mention} Flux Pavilion just dropped the bass... "I CANT STOP, OP, OP..."',
                "https://media1.tenor.com/m/p460mRpZFKAAAAAC/dubstep-virtual.gif"],
            [
                f'Presenting the {killer.mention} and {victim.mention} circus - where every match is a tightrope walk of accidental takedowns.',
                "https://media1.tenor.com/m/H_0snmBb6ooAAAAd/i-love-lucy-shookt.gif"],
            [
                f'Is it strategy or is it chaos? {killer.mention} blurs the lines with {victim.mention} caught in the crossfire.',
                "https://media1.tenor.com/m/tTEkzwUcCI4AAAAC/homer-simpson-caught-in-the-crossfire-crossfire.gif"],
            [
                f'In the world of accidental eliminations, {killer.mention} channels their inner Private Pile on {victim.mention}',
                "https://media1.tenor.com/m/1If7h96cEwMAAAAd/full-metal-jacket-vincent.gif"],
            [f'{killer.mention} gave {victim.mention} a warriors death.',
             "https://media1.tenor.com/m/E_Vj-xkWCe4AAAAd/never-give-up-monty.gif"],
            [f'{killer.mention}, you killed {victim.mention}! Oh my god, you bastard!',
             "https://media1.tenor.com/m/6ll-AoP1rbkAAAAC/oh-my-god-they-killed-kenny-you-bastards.gif"],
            [f'{killer.mention} ait {victim.mention}\'s lunch.',
             "https://media1.tenor.com/m/exg-5PtJsxsAAAAC/ronswanson-parksandrec.gif"],
            [f'{killer.mention} had a Nam flashback and {victim.mention} looked like the charlie.',
             "https://media.tenor.com/9DlIOu67gyQAAAAM/vietnam-cats.gif"],
            [f'{killer.mention} just bulldozed {victim.mention} in true Jibby fashion. He would be so proud.',
             "https://media1.tenor.com/m/z2YFVt1kZPgAAAAd/killdozer-granby.gif"],
            [f'{killer.mention} gave {victim.mention} the Old Yeller treatment.',
             "https://media1.tenor.com/m/SQjR-ybf24EAAAAC/eat-shit-robot-chicken.gif"]
        ]

        rng = random.randint(0, (len(tk_messages) - 1))
        status_add_kill, tk_object = add_teamkill(killer, victim, req_obj.guild, note)
        tk_occurence = tk_object.get_datetime().strftime("%m/%d/%y @ %I:%M %p")

        if status_add_kill:
            card = discord.Embed(title='Teamkill Logged!', color=discord.Colour.random(),
                                 description=tk_messages[rng][0])
            card.add_field(name='Teamkill ID', value=tk_object.get_auto_id(), inline=True)
            card.add_field(name="Killer", value=killer.mention, inline=True)
            card.add_field(name="Victim", value=victim.mention, inline=True)
            card.set_image(url=tk_messages[rng][1])
            card.set_footer(text=f'Reported by {req_obj.user.display_name} - {tk_occurence}',
                            icon_url=req_obj.user.avatar)
            note_set = tk_object.get_note()
            if note_set is not None:
                card.add_field(name='Note', value=tk_object.get_note(), inline=False)
            await req_obj.response.send_message(embed=card)
        else:
            await req_obj.response.send_message(
                f"There was an error adding the TK please contact the TK Bot Administrator.")

    @tk.error
    async def tk_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # async def tk_remove(ctx, killer, victim, kill_id):
    @bot.tree.command(name='remove_tk',
                      description="Removes the teamkill with the specified ID from the Tracker. Requires: Kick Members permission")
    @app_commands.checks.has_permissions(move_members=True)
    async def remove_tk(req_obj: discord.Interaction, kill_id: int):
        rm_tk_status = delete_tk(kill_id)
        if rm_tk_status:
            await req_obj.response.send_message(f"Kill ID: {kill_id} was successfully removed from the tracker.")
        else:
            await req_obj.response.send_message(
                f"Kill ID: {kill_id} encountered an error while attempt to remove from the tracker.")

    @remove_tk.error
    async def remove_tk_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # Runs the discord client
    bot.run(TOKEN)
