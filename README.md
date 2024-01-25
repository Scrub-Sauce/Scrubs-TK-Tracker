# Scrub's TK Tracker Discord Bot

Scrub's TK Tracker is a Discord bot designed to track team kills in FPS games within Discord communities. It provides a range of commands to manage and display team kill data.

## Table of Contents

- [Commands](#commands)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Commands
### Add Team kill
`/tk <@Killer> <@Victim> [Note]`
Adds a team kill to the tracker. The note attribute is optional and can be used for explanations.

![Usage of Add TK](https://i.imgur.com/uCkc4IX.png)
### Leaderboard Top 15
`/leaderboard` or `/top15`
Displays a table of the top 15 team killers on this Discord server.

![Usage of Leaderboard/Top15](https://i.imgur.com/cZkxZgD.png)
### History
`/history <@Killer>`
Displays the kill log for the mentioned player.

![Usage of History](https://i.imgur.com/jSV4e5v.png)
### Server History
`/server_history`
Displays all kills logged on this server.

![Usage of Server History](https://i.imgur.com/UWF4SsS.png)
### Bot Info
`/bot_info`
Displays information about the bot's development.

![Usage of Bot Info](https://i.imgur.com/m4WCjzV.png)
### Invite Me
`/invite_me`
Provides the user with a link to invite this bot to their Discord.

![Usage of Invite Me](https://i.imgur.com/mEvw5iJ.png)
### Report Bug
`/report_bug <Command> <Issue>`
Reports a bug to the developer. Command should be the exact command that caused the bug, and Issue should explain in detail what happened.

![Usage of Report Bug](https://i.imgur.com/4E7eE8D.png)
### Remove Team Kill
`/remove_tk <Kill ID>`
Removes the specified team kill from the bot. Requires 'Move Member' permissions.

![Usage of Remove Team Kill](https://i.imgur.com/WqpnCtu.png)
### Wipe Tracker
`/wipe_bot <Are You Sure>`
Wipes the team kill tracker of all logged kills. Requires 'Administrator' permissions. `are_you_sure` must be 'Yes' to confirm.

![Usage of Wipe Tracker](https://i.imgur.com/YRi3AsM.png)
### Help
`/help`
Displays all available commands and the context in which they can be used. You just used it...

![Usage of Help](https://i.imgur.com/eNx49wS.png)

[Usage Collection](https://imgur.com/a/0Im7H4J)
## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/scrubs-tk-tracker.git
```
1. Install the required dependencies
`pip install -r requirements.txt`
2. Set up your environment variables in a .env file:
```.env
DISCORD_TOKEN=your_discord_bot_token
DB_HOST=your_database_host
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```
## Dependencies
- Discord
- python-dotenv
- mysql-connector-python
- pytz
## Usage
1. Run the bot:
`python main.py`
2. Invite the bot to your Discord Server using the URL provided in the Developer Portal.
## Configuration
Make sure to set up your environment variables in the `.env` file as described in the Installation section.
## Contributing
Feel free to contribute to the project! Fork the repository and create a pull request.
## License
This project is licensed under the [MIT License](LICENSE).