import os
import discord
import random
from discord.ext.commands import bot
from controller.Bot_Controller import *
from model.Teamkill import Teamkill
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
from view.Server_History_View import Server_History_View as SHV


def run_bot():
    intents = discord.Intents.all()

    # Loads the Discord token from .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Creates the discord Client
    bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

    # Informs the user when running and changes the status
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        await bot.change_presence(activity=discord.CustomActivity(name=f'Try /help for commands'))
        print(f'{bot.user} has connected to Discord!')

    # Bot Invite Command
    @bot.tree.command(name='invite_me', description='Like this bot? Invite it to your Discord!')
    async def invite_me(req_obj: discord.Interaction):
        card = discord.Embed(title="Invite this bot to your discord!",
                             description='Click the link above to invite me to your discord!',
                             color=discord.Color.random(),
                             url='https://discord.com/api/oauth2/authorize?client_id=1196557331966734366&permissions=1084479764544&scope=bot')
        card.set_thumbnail(url='https://i.imgur.com/ReOfs0G.png')
        await req_obj.response.send_message(embed=card, ephemeral=True)

    # Invite Error
    @invite_me.error
    async def history_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='report_bug', description='Report a bug to the developer of this bot.')
    async def report_bug(req_obj: discord.Interaction, command: str, issue: str):
        br_status = create_bug_report(req_obj.user, req_obj.guild, command, issue)
        if br_status:
            await req_obj.response.send_message('Bug report successfully created. Thank you for your contribution.',
                                                ephemeral=True)
        else:
            await req_obj.response.send_message('Error encountered creating the bug report.', ephemeral=True)

    @report_bug.error
    async def report_bug_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='server_history')
    async def server_history(req_obj: discord.Interaction):
        status_sh, sh_data = get_server_history(req_obj.guild)
        if status_sh:
            sh_view = SHV(req_obj, sh_data, req_obj.guild.name, len(sh_data))
            await sh_view.display_embed()
        else:
            await req_obj.response.send_message(content='There is no server history yet.')

    @server_history.error
    async def server_history_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='bot_info', description='Bot information')
    async def bot_info(req_obj: discord.Interaction):
        card = discord.Embed(title='Scrub\'s TK Bot Information', description='v1.0.5', color=discord.Color.random())
        card.set_thumbnail(url='https://i.imgur.com/ReOfs0G.png')
        card.add_field(name='Developer', value='Scrub Sauce', inline=True)
        card.add_field(name='GitHub', value='**[GitHub Repo](https://github.com/Scrub-Sauce/Scrubs-TK-Tracker)**',
                       inline=True)
        card.add_field(
            name='Legal',
            value='**[Terms of Service](https://github.com/Scrub-Sauce/Scrubs-TK-Tracker/blob/main/TERMS_OF_SERVICE.md)** - **[Privacy Policy](https://github.com/Scrub-Sauce/Scrubs-TK-Tracker/blob/main/PRIVACY_POLICY.md)** - **[License](https://github.com/Scrub-Sauce/Scrubs-TK-Tracker/blob/main/LICENSE)**',
            inline=False)

        card.add_field(
            name='Gratuity',
            value='Enjoying the bot? :thumbsup:\nWant to show your support, **[Buy me a Coffee! :coffee:](https://www.buymeacoffee.com/scrub_sauce)**',
            inline=False)
        await req_obj.response.send_message(embed=card)

    @bot_info.error
    async def bot_info_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # History Command
    @bot.tree.command(name='history', description='Displays the kill log for the mentioned player.')
    async def history(req_obj: discord.Interaction, killer: discord.Member):
        k_h_status, k_h_data = get_kill_history(killer)
        d_h_status, d_h_data = get_death_history(killer)
        if k_h_status:
            card = discord.Embed(title=f'{killer.display_name} Team Kill History',
                                 description=f'The following is the log of all past team kills by {killer.display_name}',
                                 color=discord.Color.random())
            card.add_field(name='Killer', value=f'<@{killer.id}>', inline=True)
            card.add_field(name='Kill Count', value=f'{k_h_data[0]}', inline=True)
            card.add_field(name='Death Count', value=f'{d_h_data[0]}', inline=True)
            card.add_field(name='Kill History', value='', inline=False)
            kill_data = k_h_data[1]
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
            card.add_field(name='----------------------------------------', value='', inline=False)
            card.add_field(name='Death History', value='', inline=False)
            death_data = d_h_data[1]
            for line in death_data:
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

    # History Error
    @history.error
    async def history_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # Help Command
    @bot.tree.command(name='help',
                      description='Displays all available commands and the context in which they can be used.')
    async def help(req_obj: discord.Interaction):
        card = discord.Embed(title="Help", description="Here are all available commands and how they can be used.",
                             color=discord.Colour.random())
        card.add_field(name="Add Team kill",
                       value="`/tk` `<@Killer>` `<@Victim>` `[Note]` - Adds a teamkill to the tracker. The note attribute is optional and can be used for explinations",
                       inline=False)
        card.add_field(name="Leaderboard Top 15",
                       value="`/leaderboard` or `/top15` - Displays a table of the top 15 team killers on this discord server.",
                       inline=False)
        card.add_field(name="History", value="`/history` `<@Killer>` - Displays the kill log for the mentioned player.",
                       inline=False)
        card.add_field(name="Server History", value="`/server_history` - Displays all kills logged on this server.",
                       inline=False)
        card.add_field(name="Bot Info", value="`/bot_info` - Displays information about the bots development",
                       inline=False)
        card.add_field(name="Invite Me",
                       value="`/invite_me` - Provides the user with a link to invite this bot to their discords.",
                       inline=False)
        card.add_field(name="Report Bug",
                       value="`/report_bug` `<Command>` `<Issue>` - Reports bug to the developer. Command should be the exact command that cause the bug, and Issue should explain in detail what happened.",
                       inline=False)
        card.add_field(name="Remove Team kill",
                       value="`/remove_tk` `<Kill ID>` - Removes the specified team kill from the bot. Requires 'Move Member' permissions.",
                       inline=False)
        card.add_field(name="Wipe Tracker",
                       value="`/wipe_bot` `<Are You Sure>` - Wipes the team kill tracker of all logged kills. Requires 'Adminstrator' permisions. are_you_sure must be 'Yes' to confirm.",
                       inline=False)
        card.add_field(name="Help",
                       value="`/help` Displays all available commands and the context in which they can be used. You just used it...",
                       inline=False)
        await req_obj.response.send_message(embed=card)

    # Help Error
    @help.error
    async def help_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # Wipe Bot Command
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

    # Wipe Bot Error
    @wipe_bot.error
    async def wipe_bot_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    @bot.tree.command(name='leaderboard', description='Displays the a leaderboard of the top 15 team killers')
    async def leaderboard(req_obj: discord.Interaction):
        lb_status, lb_data = get_leaderboard_data(req_obj.guild)
        if lb_status:
            card = discord.Embed(title=f'{req_obj.guild.name} - Top 15 Team Killers',
                                 description='Here are your biggest shitters', color=discord.Colour.random())
            for i in range(0, len(lb_data)):
                card.add_field(name='',
                               value=f'**{i + 1}**. <@{lb_data[i][0]}> - **Kill Count:** {lb_data[i][1]} - **Death Count:** {lb_data[i][2]}',
                               inline=False)
            await req_obj.response.send_message(embed=card)
        else:
            await req_obj.response.send_message(f"Unable to display leaderboard at this time.")

    @leaderboard.error
    async def leaderboard_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # Top15 Command
    @bot.tree.command(name='top15', description='Displays the a leaderboard of the top 15 team killers')
    async def top15(req_obj: discord.Interaction):
        lb_status, lb_data = get_leaderboard_data(req_obj.guild)
        if lb_status:
            card = discord.Embed(title=f'{req_obj.guild.name} - Top 15 Team Killers',
                                 description='Here are your biggest shitters', color=discord.Colour.random())
            for i in range(0, len(lb_data)):
                card.add_field(name='',
                               value=f'**{i + 1}**. <@{lb_data[i][0]}> - **Kill Count:** {lb_data[i][1]} - **Death Count:** {lb_data[i][2]}',
                               inline=False)
            await req_obj.response.send_message(embed=card)
        else:
            await req_obj.response.send_message(f"Unable to display leaderboard at this time.")

    # Top15 Error
    @top15.error
    async def top15_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # TK Command
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
             "https://media1.tenor.com/m/SQjR-ybf24EAAAAC/eat-shit-robot-chicken.gif"],
            [f'{killer.mention} filled {victim.mention} with freedom seeds.',
             "https://c.tenor.com/gZd47MPpZ0QAAAAC/tenor.gif"],
            [f'{killer.mention} put {victim.mention} to bed for the raid.',
             "https://c.tenor.com/IYLXdzA1pgMAAAAC/tenor.gif"],
            [f'{killer.mention} got a little trigger happy and {victim.mention} was the party girl on the receiving end.',
             "https://c.tenor.com/dMLeIy2buNQAAAAC/tenor.gif"],
            [f'{killer.mention} told {victim.mention} to stop resisting. He didn\'t comply...',
             "https://c.tenor.com/MaJ4iVJSY0gAAAAC/tenor.gif"],
            [f'{killer.mention} decided to test out his new glock switch. Probably would have been a good idea for {victim.mention} to stay behind him for that.',
             "https://c.tenor.com/fOtAz-KwXZEAAAAd/tenor.gif"],
            [f'King {killer.mention} gave {victim.mention} the Anne Boleyn treatment. Ned Stark flinched in his grave',
             "https://c.tenor.com/9W632RhFORgAAAAC/tenor.gif"],
            [f'{killer.mention} decided he belonged on the iron throne and {victim.mention} was the main protagonist',
             "https://c.tenor.com/NIRQWmpfj1UAAAAC/tenor.gif"],
            [f'{killer.mention} treated {victim.mention} like Theon Greyjoy\'s pecker.',
             "https://c.tenor.com/i5kWoNobsdAAAAAC/tenor.gif"],
            [f'Yes, {killer.mention} is as sharp as he looks. He just proved that to {victim.mention}.',
             "https://c.tenor.com/exBdc7noUSoAAAAd/tenor.gif"],
            [f'{killer.mention} was a little too amped for the fight and roasted {victim.mention}',
             "https://c.tenor.com/dqbIYjcy9h4AAAAd/tenor.gif"]
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

    # TK Error
    @tk.error
    async def tk_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # Remove TK Command
    @bot.tree.command(name='remove_tk',
                      description="Removes the teamkill with the specified ID from the Tracker. Requires: Kick Members permission")
    @app_commands.checks.has_permissions(move_members=True)
    async def remove_tk(req_obj: discord.Interaction, kill_id: int):
        rm_tk_status = remove_tk_from_log(kill_id, req_obj.guild)
        if rm_tk_status:
            await req_obj.response.send_message(f"Kill ID: {kill_id} was successfully removed from the tracker.")
        else:
            await req_obj.response.send_message(
                f"Kill ID: {kill_id} encountered an error while attempt to remove from the tracker.")

    # Remove TK Error
    @remove_tk.error
    async def remove_tk_error(req_obj: discord.Interaction, error: app_commands.AppCommandError):
        await req_obj.response.send_message(content=str(error), ephemeral=True)

    # Runs the discord client
    bot.run(TOKEN)
