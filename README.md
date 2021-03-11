HockeyStatsBot

A Discord Bot that uses the NHL API in order to pull live updating hockey stats.

URL where all this data can be viewed: https://statsapi.web.nhl.com/api/v1/teams

URL to add the Discord Bot: 
https://discord.com/api/oauth2/authorize?client_id=735215611256373389&permissions=18432&scope=bot

Once the bot has been added, there are two commands to be run.
1. HS-info - This returns all the commands and all relevant information regarding the command. It is currently a Word document, however plans are in place to rework it for version 1.4 of the bot.
2. HS-setTimezone - The bot defaults to Mountain time. You can set change it to one of the 4 main time zones of the NHL. Those being: "ET" for Eastern, "CT" for Central, "MT" for Mountain, "PT" for Pacific. The command will look like: "HS-setTimezone PT"