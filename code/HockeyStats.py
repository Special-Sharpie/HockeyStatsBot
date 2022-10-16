import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import requests
import datetime
import pytz
import hockeyPy
import last
import next
import playoffData
import botLogic
import standings
import gameDay
import winloss
import teamWinLoss
import playerStats
import playoffBracket
import daySummery
import Career
import sched
import statsPerGame
import DraftYear
import playerInfo
import teamInfo
import statLeaders as sl
import nonActivePlayerCareer as non

#Variables
client = commands.Bot(command_prefix='HS-')
slash = SlashCommand(client, sync_commands=True)
game = discord.Game("/whatsnew | /settimezone | /donate")
activeTeams = ['NJD', 'NYI', 'NYR', 'PHI', 'PIT', 'BOS', 'BUF', 'MTL', 'OTT', 'TOR', 'CAR', 'FLA', 'TBL', 'WSH', 'CHI', 'DET', 'NSH', 'STL', 'CGY', 'COL', 'EDM', 'VAN', 'ANA', 'DAL', 'LAK', 'SJS', 'CBJ', 'MIN', 'WPG', 'ARI', 'VGK', 'SEA']


#Events:
@client.event
async def on_ready():
    print('The world is calling {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_command_error(ctx, error):
    #Error Handling!
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        e = discord.Embed(title = "An Error Has Occured!", description='Rquested command is missing one more key parameters.\nPlease retry the commmand with the proper paramerters. \n Run "?info", for more information!', colour= discord.Colour.from_rgb(0, 0, 0))
        e.add_field(name= 'Error Code:', value= 'MissingRequiredArgument', inline= True)
        e.set_footer(text= 'This is an automatic error handler. Feel free to delete this message!')
        await ctx.channel.send('', embed= e)
    if isinstance(error, commands.CommandNotFound):
        e = discord.Embed(title = "An Error Has Occured!", description='An Unknown command was requested!\nRun "?info" for a list of commands!', colour= discord.Colour.from_rgb(0, 0, 0))
        e.add_field(name= 'Error Code:', value= 'CommandNotFound', inline= True)
        e.set_footer(text= 'This is an automatic error handler. Feel free to delete this message!')
        await ctx.channel.send('', embed= e)
    if isinstance(error, commands.CommandInvokeError):
        e = discord.Embed(title="An Error Has Occured!", description='Please check your spelling of all required parameters, or verify that only the required parameters where provided!\nRun "?info" for a list of commands!', colour= discord.Colour.from_rgb(0, 0, 0))
        e.add_field(name='Error Code:', value='CommandInvokeError', inline=True)
        e.set_footer(text='This is an automatic error handler. Feel free to delete this message!')
        await ctx.channel.send('', embed=e)

#Commands
@slash.slash(name="serverCount", description="Show how many servers the bot provideds hockey stats to!", options=[])
@client.command()
async def serverCount(ctx):
    await ctx.reply(f'Currently providing hockey stats to {len(client.guilds)} servers!')

@client.event
async def on_guild_join(ctx):
    guildID = ctx.id
    botLogic.writeJSON('ServerTimezone.json', guildID, 'MT')

#Commands
@slash.slash(
    name="settimezone", 
    description="Changes the set server timezone", 
    options= [ 
        create_option(
            name="timezone", 
            description="The timezone code", 
            option_type=3, 
            required=True,
            choices=[
                create_choice(name="Mountain Time", value="MT"),
                create_choice(name="Pacific Time", value="PT"),
                create_choice(name="Central Time", value="CT"),
                create_choice(name="Eastern Time", value="ET"),
                create_choice(name="Central European Time", value="CET"),
                create_choice(name="Eastern European Time", value="EET"),
                create_choice(name="Western European Time", value="WET"),
            ]
        )]
    )
@client.command()
@commands.has_permissions(administrator=True)
async def setTimezone(ctx, timezone):
    timezones = ["MT", "PT", "CT", "ET", "CET", "EET", "WET"]
    if timezone in timezones:
        guildID = ctx.guild.id
        botLogic.writeJSON('ServerTimezone.json', guildID, timezone)
        await ctx.reply('Timezone set to {}'.format(timezone))
    else:
        await ctx.reply('Yeah that timezone is far to complex for my small brained creator.')

@slash.slash(
    name="skatercareer", 
    description="Provides all stats of a player from every season, and their totals!", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player. Format: CaleMakar. SabatianAho: Use SabatianAhoSWE or SabatianAhoFIN", 
            option_type=3, 
            required=True
        )])
@client.command()
async def skaterCareer(ctx, playername):
    await ctx.defer()
    playerID = botLogic.readJSON('Player.json', playername)
    playername = botLogic.GetPlayerName(playerID)
    x = Career.skaterStats(str(playerID))
    if len(x[1]) < 1024:
        e = discord.Embed(title="Career Stats - {}".format(playername))
        e.add_field(name=x[0], value= x[1])
        e.set_footer(text=x[2])
        await ctx.channel.send('', embed= e)
    else:
        await  ctx.channel.send('Career Stats - {}\n'.format(playername) + x[0] +'\n' + x[1] + '\n' + x[2])

@slash.slash(
    name="teamwl", 
    description="Provides the current seasons record of the requested team!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
            )
        ])
@client.command()
async def teamWL(ctx, abbr):
    await ctx.defer()
    abbr = abbr.upper()
    ID = botLogic.readJSON('ABBRid.json', abbr)
    y = botLogic.readJSON('TeamColour.json', ID)
    season = botLogic.GetCurrentSeason()
    x = teamWinLoss.WinLossTeam(ID)
    e = discord.Embed(title= 'Single Season Win/Loss!', description= 'The ' + season[:4] + '-' + season[4:] +' Win/Loss record for the ' + x[0], colour= discord.Colour.from_rgb(y[0], y[1], y[2]))
    e.add_field(name= 'Record:', value= str(x[2]) + '/' + str(x[3]) + '/' + str(x[4]) + ' in ' + str(x[1]) + ' games, tallying ' + str(x[5]) + ' points.')
    await ctx.reply('', embed= e)

@slash.slash(
    name="currentseason", 
    description="Provides the current season!", 
    options= [])
@client.command()
async def currentSeason(ctx):
    x = botLogic.GetCurrentSeason()
    await ctx.reply("Its currently the {}-{} season".format(x[:4], x[4:]))

@client.command()
async def teamID(ctx):
    with open('TeamID.txt', 'r') as f:
        x = f.read()
        await ctx.author.send(x)

@slash.slash(
    name="lifewl", 
    description="Provides the lifetime win/loss between two teams!", 
    options= [
        create_option(
            name="abbr1", 
            description="The first team to compare", 
            option_type=3, 
            required=True
        ), create_option(
            name="abbr2",
            description="The second team to compare" ,
            option_type=3,
            required=True 
        )
    ])

@client.command()
async def lifeWL(ctx, abbr1, abbr2):
    await ctx.defer()
    abbr1 = abbr1.upper()
    abbr2 = abbr2.upper()
    FranID1 = botLogic.readJSON('ABBRid.json', abbr1)
    FranID2 = botLogic.readJSON('ABBRid.json', abbr2)
    r, g, b = botLogic.readJSON('TeamColour.json', FranID1)
    x = winloss.winloss(FranID1, FranID2)
    e = discord.Embed(title= 'Life Time Win/loss!', description= 'The lifetime Win/Loss/OT/T \n' + x[0] + ' VS. ' + x[1], colour= discord.Colour.from_rgb(r, g, b))
    e.add_field(name= 'Home Record:', value= str(x[2]) + '/' + str(x[3]) + '/' + str(x[4]) + '/' + str(x[5]), inline= False)
    e.add_field(name= 'Road Record:', value= str(x[6]) + '/' + str(x[7]) + '/' + str(x[8]) + '/' + str(x[9]), inline= False)
    e.add_field(name= 'Total Record:', value= str(x[10]) + '/' + str(x[11]) + '/' + str(x[12]) + '/' + str(x[13]), inline= False)
    await ctx.reply('', embed= e)

@slash.slash(
    name="pstats", 
    description="Provides the players stat/game of the requested season!", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player. Format: CaleMakar. SabatianAho: Use SabatianAhoSWE or SabatianAhoFIN", 
            option_type=3, 
            required=True
        ), create_option(
            name="season",
            description="Changes the season that stat is pulled from. Defaults to current season" ,
            option_type=3,
            required=False 
        ), create_option(
            name="stat",
            description="Changes the season type of the stats provided. Defaults to regualar season." ,
            option_type=3,
            required=False,
            choices = [
                create_choice(name='Regular Season', value='R'),
                create_choice(name='Playoffs', value='P')
            ]),
    ])
@client.command()
async def Pstats(ctx, playername, season= botLogic.GetCurrentSeason(), playoff= 'R',):
    await ctx.defer()
    playerID = botLogic.readJSON('Player.json', playername)
    if playoff == "R":
        x = playerStats.stats(playerID, playoff, season)
        e = discord.Embed(title= 'Single Season Stats - ' + season[:4] +'-'+ season[4:], description= 'Stats for ' + x[0], colour= discord.Colour.from_rgb(0,0,0))
        e.add_field(name='Stats:', value= x[1], inline= False)
        await ctx.reply('', embed= e)
    elif playoff == 'P':
        x = playerStats.stats(playerID, playoff, season)
        e = discord.Embed(title= 'Post Season Stats - ' + season[4:] + ' Stanley Cup Playoffs', description= 'Stats for ' + x[0], colour= discord.Colour.from_rgb(0,0,0))
        e.add_field(name='Stats:', value= x[1], inline= False)
        await ctx.reply('', embed= e)

@slash.slash(
    name="perGame", 
    description="Provides the players stat/game of the requested season!", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player. Format: CaleMakar. SabatianAho: Use SabatianAhoSWE or SabatianAhoFIN", 
            option_type=3, 
            required=True
        ), create_option(
            name="stat",
            description="Changes the stat that is compared per game." ,
            option_type=3,
            required=True,
            choices = [
                create_choice(name='Assists', value='assists'),
                create_choice(name='Goals', value='goals'),
                create_choice(name='Points', value='points'),
                create_choice(name='Penalty Infraction Minutes', value='pim'),
                create_choice(name='Shots', value='shots'),
                create_choice(name='Hits', value='hits'),
                create_choice(name='Power Play Goals', value='powerPlayGoals'),
                create_choice(name='Power Play Points', value='powerPlayPoints'),
                create_choice(name='Penalty Minutes', value='penaltyMinutes'),
                create_choice(name='Faceoff Percentage', value='faceOffPct'),
                create_choice(name='Shot Percentage', value='shotPct'),
                create_choice(name='Game Winning Goals', value='gameWinningGoals'),
                create_choice(name='Overtime Goals', value='overTimeGoals'),
                create_choice(name='Short Handed Goals', value='shortHandedGoals'),
                create_choice(name='Short Handed Points', value='shortHandedPoints'),
                create_choice(name='Blocked', value='blocked'),
                create_choice(name='Plus/Minus', value='plusMinus'),
                create_choice(name='Shifts', value='shifts')
            ]), create_option(
            name="season",
            description="Changes the season that stat is pulled from. Defaults to current season" ,
            option_type=4,
            required=False 
        )
    ])
@client.command()
async def perGame(ctx, playername, stat, season= botLogic.GetCurrentSeason()):
    await ctx.defer()
    playerID = botLogic.readJSON('Player.json', playername)
    playername = botLogic.GetPlayerName(playerID)
    statName, statAvg, rawStat, games = statsPerGame.statsPerGameCalculator(playerID, stat, season)
    x = statsPerGame.statsPerGameCalculator(playerID, stat, season)
    e = discord.Embed(
                    title= '{} Per Game - {}'.format(statName, playername),
                    description='{} per Game: {} \n Total {}: {}\nTotal Games: {}'.format(statName, statAvg, statName, rawStat, games),
                    colour= discord.Colour.from_rgb(0,0,0)
                    )
    await ctx.reply('', embed=e)

#Commands for individual PLayer/Goalie Stats

#Goalies:
@client.command()
async def Gotl(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieOT = stats_url.json()['stats'][0]['splits'][0]['stat']['ot']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Overtime losses - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has lost ' + str(goalieOT) + ' games in Overtime so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Overtime losses - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' lost ' + str(goalieOT) + ' games in Overtime during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    
@client.command()
async def Gwins(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieWins = stats_url.json()['stats'][0]['splits'][0]['stat']['wins']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Wins - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has won ' + str(goalieWins) + ' games so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Wins - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' won ' + str(goalieWins) + ' games in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Gloss(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieLosses = stats_url.json()['stats'][0]['splits'][0]['stat']['losses']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Losses - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has lost ' + str(goalieLosses) + ' games so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Losses - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' lost ' + str(goalieLosses) + ' games in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Gsaves(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieSaves = stats_url.json()['stats'][0]['splits'][0]['stat']['saves']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Saves - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has made ' + str(goalieSaves) + ' saves so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Saves - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' made ' + str(goalieSaves) + ' save in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Gtoi(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieTOI = stats_url.json()['stats'][0]['splits'][0]['stat']['timeOnIce']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Time On Ice - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has ' + str(goalieTOI) + ' minutes on the ice so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

    else:
        e = discord.Embed(title= 'Time On Ice - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' played a total of ' + str(goalieTOI) + ' minutes during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Gshutout(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieSO = stats_url.json()['stats'][0]['splits'][0]['stat']['shutouts']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Shutouts - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has ' + str(goalieSO) + ' Shutouts so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Shutouts - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' made ' + str(goalieSO) + ' Shutouts in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Gsavep(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieSP = stats_url.json()['stats'][0]['splits'][0]['stat']['savePercentage']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Save Percentage - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has a ' + str(goalieSP) + ' Save Percentage so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Save Percentage - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' had a ' + str(goalieSP) + ' Save Percentage in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Ggaa(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieGAA = stats_url.json()['stats'][0]['splits'][0]['stat']['goalAgainstAverage']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Goals Against Average - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has a ' + str(goalieGAA) + ' Goal Against Average so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Goals Against Average - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' had a ' + str(goalieGAA) + ' Goal Against Average in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)


@client.command()
async def Ggames(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieGames = stats_url.json()['stats'][0]['splits'][0]['stat']['games']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Games Played - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has played in ' + str(goalieGames) + ' games so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Games Played - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' played in ' + str(goalieGames) + ' games in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Gshota(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieSA = stats_url.json()['stats'][0]['splits'][0]['stat']['shotsAgainst']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Shots Against - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has faced ' + str(goalieSA) + ' shots so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Shots Against - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' faced ' + str(goalieSA) + ' shots in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Ggoala(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieGA = stats_url.json()['stats'][0]['splits'][0]['stat']['goalsAgainst']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Goals Against - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has been scored on ' + str(goalieGA) + ' times so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Goals Against - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' was scored on ' + str(goalieGA) + ' times in the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

#Players:
@client.command()
async def Pgoals(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerGoal = stats_url.json()['stats'][0]['splits'][0]['stat']['goals']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                          description=botLogic.GetPlayerName(playerID) + ' has scored ' + str(playerGoal) + ' goals so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' scored ' + str(playerGoal) + ' goals during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Passists(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerAssists = stats_url.json()['stats'][0]['splits'][0]['stat']['assists']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Assists - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has ' + str(playerAssists) + ' assists so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Assists - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' had ' + str(playerAssists) + ' assists during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Ppoints(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerPoints = stats_url.json()['stats'][0]['splits'][0]['stat']['points']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Points - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has ' + str(playerPoints) + ' points so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Points - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' had ' + str(playerPoints) + ' points during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
@client.command()
async def Pshots(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerShots = stats_url.json()['stats'][0]['splits'][0]['stat']['shots']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Shots - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has taken ' + str(playerShots) + ' shots so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Shots - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' took ' + str(playerShots) + ' shots during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Pplusminus(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerPM = stats_url.json()['stats'][0]['splits'][0]['stat']['plusMinus']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Plus/Minus - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has a plus/minus rating of ' + str(playerPM) + ' so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Plus/Minus - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' had a plus/minus rating of ' + str(playerPM) + ' during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Ptoi(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerTOI = stats_url.json()['stats'][0]['splits'][0]['stat']['timeOnIce']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Time On Ice - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has ' + str(playerTOI) + ' minutes on the ice so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Time On Ice - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' played a total of ' + str(playerTOI) + ' minutes during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Pgplayed(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerGames = stats_url.json()['stats'][0]['splits'][0]['stat']['games']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Games Played - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has played ' + str(playerGames) + ' games so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Games Played - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' played a total of ' + str(playerGames) + ' games during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Pppgoals(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerPPG = stats_url.json()['stats'][0]['splits'][0]['stat']['powerPlayGoals']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Power Play Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has scored ' + str(playerPPG) + ' goals on the power play so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Power Play Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' scored ' + str(playerPPG) + ' power play goals during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Ppppoints(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerPPP = stats_url.json()['stats'][0]['splits'][0]['stat']['powerPlayPoints']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Power Play Points - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has scored ' + str(playerPPP) + ' points on the power play so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Power Play Points - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' scored ' + str(playerPPP) + ' power play points during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Pgwgoals(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerGWG = stats_url.json()['stats'][0]['splits'][0]['stat']['gameWinningGoals']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Game Winning Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has scored ' + str(playerGWG) + ' game winning goals so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Game Winning Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' scored ' + str(playerGWG) + ' game winning goals during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Ppenalty(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerPIM = stats_url.json()['stats'][0]['splits'][0]['stat']['pim']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Penalty In Minutes - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has collected ' + str(playerPIM) + ' penalty minutes so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Penalty In Minutes - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' collected ' + str(playerPIM) + ' penalty minutes during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Phits(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerHits = stats_url.json()['stats'][0]['splits'][0]['stat']['hits']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Hits - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has ' + str(playerHits) + ' hits on the season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Hits - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' threw ' + str(playerHits) + ' hits during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Pbshots(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerBlocked = stats_url.json()['stats'][0]['splits'][0]['stat']['blocked']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Blocked Shots - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has blocked ' + str(playerBlocked) + ' blocked shots this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Blocked Shots - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' had blocked ' + str(playerBlocked) + ' blocked shots during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Potgoals(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerOTgoals = stats_url.json()['stats'][0]['splits'][0]['stat']['overTimeGoals']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Overtime Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has scored ' + str(playerOTgoals) + ' Overtime goals this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Overtime Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' scored ' + str(playerOTgoals) + ' Overtime goals during the ' + season[:4] +'-'+ season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@client.command()
async def Pshgoals(ctx, playername, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', playername)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    playerShortHanded = stats_url.json()['stats'][0]['splits'][0]['stat']['shortHandedGoals']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Short Handed Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has scored ' + str(playerShortHanded) + ' Short Handed goals this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Short Handed Goals - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' scored ' + str(playerShortHanded) + ' Short Handed goals during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)

@slash.slash(
    name="gnext", 
    description="Provides all the details for the next game, within 10 days, of the requested team!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
            )
        ])
@client.command()
async def Gnext(ctx, abbr):
    await ctx.defer()
    abbr = abbr.upper()
    guildID = ctx.guild.id
    teamID = botLogic.readJSON('ABBRid.json', abbr)
    r, g, b = botLogic.readJSON('TeamColour.json', teamID)
    TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
    x = next.next(teamID, TZ)
    e = discord.Embed(title= 'Next Game!', description= x, colour= discord.Colour.from_rgb(r, g, b))
    await ctx.reply('', embed= e)

@slash.slash(
    name="next7", 
    description="Provides the requested teams schedule over the following 7 days!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
            )
        ])

@client.command()
async def next7(ctx, abbr):
    await ctx.defer()
    abbr = abbr.upper()
    guildID = ctx.guild.id
    ID = botLogic.readJSON('ABBRid.json', abbr)
    team = botLogic.GetTeamName(ID)
    r, g, b = botLogic.readJSON('TeamColour.json', ID)
    TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
    x = sched.schedule(ID, TZ)
    e = discord.Embed(title='7 Day Schedule - {}'.format(team), colour= discord.Colour.from_rgb(r, g, b))
    for i in x:
        date = x[i]
        if type(date) == list:
            e.add_field(name=i, value='{} VS. {} at {}'.format(date[1], date[2], date[0]), inline=False)
        else:
            e.add_field(name=i, value='{}'.format(date), inline=False)
    await ctx.reply('', embed=e)

@slash.slash(
    name="glast", 
    description="Provides all the details of the last game played, within the last 10 days!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
            )
        ])
@client.command()
async def Glast(ctx, abbr):
    await ctx.defer()
    abbr = abbr.upper()
    teamID = botLogic.readJSON('ABBRid.json', abbr)
    r, g, b = botLogic.readJSON('TeamColour.json', teamID)
    x = last.last(teamID)
    if len(x) == 1:
        e = discord.Embed(title= 'Last Game Played!', description= x[0], colour= discord.Colour.from_rgb(r, g, b))
        await ctx.reply('', embed=e)
    else:
        z = botLogic.pastGameStats(teamID, x[7])
        e = discord.Embed(title='Last Game Played! - ' + x[6],description= x[0] + ' VS. ' + x[1], colour=discord.Colour.from_rgb(r, g, b))
        e.add_field(name='Overview:', value=x[4] + ': ' + x[2] + ' ' + str(z[2]) + ' SOG \n' + x[5] + ': ' + x[3] + ' ' + str(z[13]) + ' SOG', inline=False)
        e.add_field(name=x[4], value= str(z[2]) + '\n' +  str(z[6]) + '\n' + str(z[4])[:-2] + '/' + str(z[5])[:-2] + '\n' + str(z[1]) + '\n' + str(z[10]) + '\n' + str(z[7]) + '\n' + str(z[9]) + '\n' + str(z[8]), inline=True)
        e.add_field(name='Game Stats', value=' ----SOG----\n-Faceoff %-\n-Power Play-\n----PIM----\n----Hits----\n---Blocks---\n-Giveaways-\n-Takeaways-', inline=True)
        e.add_field(name=x[5], value= str(z[13]) + '\n' + str(z[17]) + '\n' + str(z[15])[:-2] + '/' + str(z[16])[:-2] + '\n' + str(z[12]) + '\n' + str(z[21]) + '\n' + str(z[18]) + '\n' + str(z[20]) + '\n' + str(z[19]), inline=True)
        m = botLogic.getGoalScorers(teamID, x[7])
        if len(m) != 0:
            for i in m:
                e.add_field(name='Goal', value=i, inline=False)
        await ctx.reply('', embed= e)

@slash.slash(
    name="gtoday", 
    description="Provides all the details needed for the requested team's current day match up!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
            )
        ])
@client.command()
async def Gtoday(ctx, abbr):
    await ctx.defer()
    abbr = abbr.upper()
    try:
        ID = botLogic.readJSON('ABBRid.json', abbr)
        guildID = ctx.guild.id
        TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
        r, g, b = botLogic.readJSON('TeamColour.json', ID)
        x = gameDay.gday(ID, TZ)
        if x[0] < '3':
            e = discord.Embed(title= 'Game Day!', description= x[1] + ' VS. ' + x[2] + ' at ' + x[3], colour= discord.Colour.from_rgb(r, g, b))
            await ctx.reply('', embed= e)
        elif x[0] > '4':
            z = botLogic.gameStats(ID)
            e = discord.Embed(title='Game Day!', description= x[1] + ' VS. ' + x[2], colour=discord.Colour.from_rgb(r, g, b))
            e.set_author(name='Status: Final')
            e.add_field(name='Overview:', value=x[3] + ': ' + x[5] + ' ' + x[7] + ' SOG \n' + x[4] + ': ' + x[6] + ' ' + x[8] + ' SOG', inline=False)
            e.add_field(name=x[3], value= str(z[2]) + '\n' +  str(z[6]) + '\n' + str(z[4])[:-2] + '/' + str(z[5])[:-2] + '\n' + str(z[1]) + '\n' + str(z[10]) + '\n' + str(z[7]) + '\n' + str(z[9]) + '\n' + str(z[8]), inline=True)
            e.add_field(name='Game Stats', value=' ----SOG----\n-Faceoff %-\n-Power Play-\n----PIM----\n----Hits----\n---Blocks---\n-Giveaways-\n-Takeaways-', inline=True)
            e.add_field(name=x[4], value= str(z[13]) + '\n' + str(z[17]) + '\n' + str(z[15])[:-2] + '/' + str(z[16])[:-2] + '\n' + str(z[12]) + '\n' + str(z[21]) + '\n' + str(z[18]) + '\n' + str(z[20]) + '\n' + str(z[19]), inline=True)
            m = botLogic.getGoalScorers(ID, x[9])
            if len(m) != 0:
                for i in m:
                    e.add_field(name='Goal', value=i, inline=False)
            await ctx.reply('', embed=e)
        else:
            gametime, period = botLogic.getGameTime(ID, x[9])
            e = discord.Embed(title='Game Day! - ' + x[1] + ' VS. ' + x[2], colour=discord.Colour.from_rgb(r, g, b))
            e.set_author(name='Status: On-going'  + ' | Time Remaining: ' + gametime + ', ' + period)
            e.add_field(name=x[1], value='Goals: ' +x[5]+ '\nShots: ' + x[7])
            e.add_field(name=x[2], value='Goals: ' +x[6]+ '\nShots: ' + x[8])
            m = botLogic.getGoalScorers(ID, x[9])
            if len(m) != 0:
                for i in m:
                    e.add_field(name='Goal', value=i, inline=False)
            await ctx.reply('', embed=e)
    except IndexError:
        team = hockeyPy.Team(abbr)
        e = discord.Embed(title='Game Day!', description=f"No {team.GetTeamName()} game today!", colour=discord.Color.from_rgb(team.colour[0], team.colour[1], team.colour[2]))
        await ctx.reply("", embed=e)

# Being re-worked as off version 2.1 (version 1.5 pre slash migration) will be migrated to slash when complete
@client.command()
async def divStandings(ctx, div):
    x = standings.div(div)
    e = discord.Embed(title= x[0][:4] + '-' + x[0][4:] +' '+ div + ' | Division Standings', description= x[1], colour= discord.Colour.from_rgb(0, 0, 0))
    await ctx.channel.send('', embed= e)

@slash.slash(
    name="confstandings", 
    description="Provides the most up to date conference standings for the current season!", 
    options= [
        create_option(
            name="conference", 
            description="Changes which conference standings provieded.", 
            option_type=3, 
            required=True,
            choices=[
                create_choice(name="Western Conference", value="Western"),
                create_choice(name="Eastern Conference", value="Eastern")
            ]
        )
    ])
@client.command()
async def confStandings(ctx, conference):
    await ctx.defer()
    x = standings.conf(conference)
    e = discord.Embed(title= x[0][:4] + '-' + x[0][4:] +' '+ conference + ' Conference Standings', description= x[1], colour= discord.Colour.from_rgb(0, 0, 0))
    await ctx.reply('', embed=e)

@slash.slash(
    name="leaguestandings", 
    description="Provides the most up to date league standings for the requested season!", 
    options= [
        create_option(
            name="season", 
            description="Changes which season the standings are from. Defaults to current season. Format: 20222023", 
            option_type=3, 
            required=False
            )
        ])
@client.command()
async def leagueStandings(ctx, season= botLogic.GetCurrentSeason()):
    await ctx.defer()
    x = standings.league(season)
    e = discord.Embed(title= x[0][:4] + '-' + x[0][4:] + ' | League Standings', description= x[1], colour= discord.Colour.from_rgb(0, 0, 0))
    await ctx.reply('', embed= e)

@slash.slash(
    name="scfwinner", 
    description="Provides the winner of the stanley in the requested season!", 
    options= [
        create_option(
            name="season", 
            description="Changes which season the stanley cup winner is from.", 
            option_type=3, 
            required=True
            )
        ])
@client.command()
async def SCFwinner(ctx, season):
    await ctx.defer()
    x = playoffData.playoffWin(season)
    r, g, b = botLogic.readJSON('TeamColour.json', x[5])
    e = discord.Embed(title= x[0] + ' ' + x[1], colour= discord.Colour.from_rgb(r, g, b))
    e.add_field(name= 'Champion:', value= 'The ' + x[2] + ' won the Stanley Cup', inline= False)
    e.add_field(name= 'Series Record:', value= x[3] + ' Wins, ' + x[4] + ' Losses', inline= True)
    await ctx.reply('', embed= e)

@slash.slash(
    name="playoffstandings", 
    description="Provides an overview of a playoff matchup of the team, in requested playoff season and round!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True
        ), create_option(
            name="round",
            description="Specifies which playoff round the matchup is in." ,
            option_type=3,
            required=True,
            choices = [
                create_choice(name='Stanley Cup Qualifier (2019-2020 Only!)', value='SQF'),
                create_choice(name='Round 1', value='R1'),
                create_choice(name='Round 2', value='R2'),
                create_choice(name='Conference Final', value='CF'),
                create_choice(name='Stanley Cup Final', value='SCF'),
            ]
        ), create_option(
            name="season",
            description="Which playoff season the matchup is in." ,
            option_type=3,
            required=True
        )
    ])
@client.command()
async def playoffStandings(ctx, abbr, round, season):
    await ctx.defer()
    abbr = abbr.upper()
    x = playoffBracket.playoffStanding(abbr, round, season)
    r, g, b = botLogic.readJSON('TeamColour.json', x[6])
    e = discord.Embed(title =  x[0][4:] + ' Playoffs - ' + x[1], colour= discord.Colour.from_rgb(r, g, b))
    e.add_field(name = 'Match Up:', value = x[2] + ' VS. ' + x[3], inline= False)
    e.add_field(name = 'Series Record:', value = x[2] + ': ' + str(x[4]) + ' ' + x[3] + ': ' + str(x[5]), inline = True)
    await ctx.reply('', embed = e)

@slash.slash(
    name="daysummary", 
    description="Provides and overview of all games of the day.", 
    options= [
        create_option(
            name="date", 
            description="Changes what day the bot returns games from. Defaults to  Format: YYYY-MM-DD", 
            option_type=3, 
            required=False
            )
        ])
@client.command()
async def daySummary(ctx, date= None):
    await ctx.defer()
    if date == None:
        isToday = True
        date = str(datetime.datetime.now(pytz.timezone('Canada/Mountain')))
    else:
        isToday = False
    date = date[:10]
    try:
        guildID = ctx.guild.id
        x = daySummery.daySumDate(date)
        formatdate = x[1]
        TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
        
        e = discord.Embed(title= 'Day Summary - ' + formatdate, colour= discord.Colour.from_rgb(0,0,0))
        i = 0
        while i < x[0]:
            z = daySummery.daySum(i, TZ, date)
            if len(z) == 7:
                e.add_field(name= z[0] + ' VS. ' + z[1], value= z[2] +': '+ str(z[4]) + ' | ' + z[3] + ': ' + str(z[5]) + ' | ' + z[6], inline= False)
            else:
                e.add_field(name= z[0] + ' VS. ' + z[1], value=z[2] + ' VS. ' + z[3] + ' | ' + z[4], inline=False)
            i += 1
        await ctx.reply('', embed= e)
    except IndexError:
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        game_dt = datetime.datetime.strftime(dt, '%A, %B %d, %Y')
        if isToday:
            await ctx.reply(f"No games today - {game_dt}")
        else:
            await ctx.reply(f"No games on {game_dt}")

@slash.slash(
    name="draftbyear", 
    description="Provides all the players drafted by the requested team in the requested year!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
        ), create_option(
            name="year", 
            description="Which draft year to look up", 
            option_type=3, 
            required=True,
            )
    ])
@client.command()
async def draftByYear(ctx, abbr, year):
    await ctx.defer()
    abbr = abbr.upper()
    teamID = botLogic.readJSON('ABBRid.json', abbr)
    teamFullName = botLogic.GetTeamName(teamID)
    r, g, b = botLogic.readJSON('TeamColour.json', teamID)
    results = DraftYear.draft(year, teamID)
    e = discord.Embed(title='{} Draft | {}'.format(year, teamFullName), colour= discord.Colour.from_rgb(r, g, b))
    for res in results:
        for draftee in results[res]:
            e.add_field(name=res, value=draftee, inline= False)
    await ctx.reply('', embed=e)

@slash.slash(
    name="pinfo", 
    description="Provides information about the requested player!", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player. Format: CaleMakar. SabatianAho: Use SabatianAhoSWE or SabatianAhoFIN", 
            option_type=3, 
            required=True
            )
        ])
@client.command()
async def Pinfo(ctx, playername):
    await ctx.defer()
    playerID = botLogic.GetPlayerID(playername)
    fullName = botLogic.GetPlayerName(playerID)
    personal = playerInfo.playerInfo(playername)
    teamBased = playerInfo.playerTeamInfo(playername)
    e = discord.Embed(title='Player Info | {}'.format(fullName), colour=discord.Colour.from_rgb(0,0,0))
    e.add_field(name='Personal', value=personal)
    e.add_field(name='Team', value=teamBased)
    await ctx.reply('', embed=e)
    # await ctx.reply("")

@slash.slash(
    name="Tinfo", 
    description="Provides information about the requested team!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True,
            )
        ])
@client.command()
async def Tinfo(ctx, abbr):
    await ctx.defer()
    abbr = abbr.upper()
    name, info, colour = teamInfo.teamInfo(abbr)
    x = teamInfo.teamInfo(abbr)
    r, g, b = colour
    e = discord.Embed(title='Team Info | {}'.format(name), description=info, colour= discord.Colour.from_rgb(r, g, b))
    await ctx.channel.send('', embed=e)

@slash.slash(
    name="statleaders", 
    description="Provides the requested number of scoring leaders of the requested stat, for the requested team!", 
    options= [
        create_option(
            name="abbr", 
            description="NHL team abbreviation.", 
            option_type=3, 
            required=True
        ), create_option(
            name="count",
            description="Changes how many players a provided. Defaults to 5." ,
            option_type=4,
            required=False 
        ), create_option(
            name="stat",
            description="Changes the stat the players are ranked by. Defaults to points." ,
            option_type=3,
            required=False,
            choices = [
                create_choice(name='Assists', value='assists'),
                create_choice(name='Goals', value='goals'),
                create_choice(name='Points', value='points'),
                create_choice(name='Penalty Infraction Minutes', value='pim'),
                create_choice(name='Shots', value='shots'),
                create_choice(name='Games Played', value='games'),
                create_choice(name='Hits', value='hits'),
                create_choice(name='Power Play Goals', value='powerPlayGoals'),
                create_choice(name='Power Play Points', value='powerPlayPoints'),
                create_choice(name='Penalty Minutes', value='penaltyMinutes'),
                create_choice(name='Faceoff Percentage', value='faceOffPct'),
                create_choice(name='Shot Percentage', value='shotPct'),
                create_choice(name='Game Winning Goals', value='gameWinningGoals'),
                create_choice(name='Overtime Goals', value='overTimeGoals'),
                create_choice(name='Short Handed Goals', value='shortHandedGoals'),
                create_choice(name='Short Handed Points', value='shortHandedPoints'),
                create_choice(name='Blocked', value='blocked'),
                create_choice(name='Plus/Minus', value='plusMinus'),
                create_choice(name='Shifts', value='shifts')
            ]
        )
    ])
@client.command()
async def statLeaders(ctx, abbr, count=5, stat='points'):
    await ctx.defer()
    abbr = abbr.upper()
    team = hockeyPy.Team(abbr)
    teamName = team.GetTeamName()
    results = sl.teamLeaders(abbr, count, stat)
    r, g, b = team.getTeamColour(team.id)
    if stat[-1] == 's':
        e = discord.Embed(title=f'{teamName} | {stat[0].upper() + stat[1:-1]} Leaders', description=results, colour= discord.Colour.from_rgb(r, g, b))
    else:
        e = discord.Embed(title=f'{teamName} | {stat[0].upper() + stat[1:]} Leaders', description=results, colour= discord.Colour.from_rgb(r, g, b))
    await ctx.reply('', embed=e)

@slash.slash(
    name="atplayerstats", 
    description="Provides a career overview of any NHL player, active or not.", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player Format: WayneGretzky", 
            option_type=3, 
            required=True,
            )
        ])
@client.command()
async def ATplayerStats(ctx, playername):
    await ctx.defer()
    playerId = botLogic.readJSON("AllTimePlayer.json", playername)
    firstYear, lastYear, fullname, stats = non.skaterStats(playerId)
    x = non.skaterStats(playerId)
    e = discord.Embed(title=f"All time player Stats | {fullname}", description=f"Active from {firstYear} to {lastYear}", colour=discord.Colour.from_rgb(0,0,0))
    e.add_field(name="Career Totals:", value=stats)
    await ctx.reply('', embed= e)

@client.command()
async def statCodes(ctx):
    with open("statCodes.txt", "r+") as f:
        codes = f.read()
        await ctx.author.send(codes + '\nCodes used for singleStats command, and perGame command.')

# Example of the use case for the Player class defined in hockeyPy.
@slash.slash(
    name="skatersinglestat", 
    description="Provides the requested number of scoring leaders of the requested stat, for the requested team!", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player. Format: CaleMakar. SabatianAho: Use SabatianAhoSWE or SabatianAhoFIN", 
            option_type=3, 
            required=True
        ), create_option(
            name="stat",
            description="Changes the stat that is returned." ,
            option_type=3,
            required=True,
            choices = [
                create_choice(name='Assists', value='assists'),
                create_choice(name='Goals', value='goals'),
                create_choice(name='Points', value='points'),
                create_choice(name='Time On Ice', value='timeOnIce'),
                create_choice(name='Penalty Infraction Minutes', value='pim'),
                create_choice(name='Shots', value='shots'),
                create_choice(name='Games Played', value='games'),
                create_choice(name='Hits', value='hits'),
                create_choice(name='Power Play Goals', value='powerPlayGoals'),
                create_choice(name='Power Play Points', value='powerPlayPoints'),
                create_choice(name='Power Play Time On Ice', value='powerPlayTimeOnIce'),
                create_choice(name='Even Time On Ice', value='evenTimeOnIce'),
                create_choice(name='Penalty Minutes', value='penaltyMinutes'),
                create_choice(name='Faceoff Percentage', value='faceOffPct'),
                create_choice(name='Shot Percentage', value='shotPct'),
                create_choice(name='Game Winning Goals', value='gameWinningGoals'),
                create_choice(name='Overtime Goals', value='overTimeGoals'),
                create_choice(name='Short Handed Goals', value='shortHandedGoals'),
                create_choice(name='Short Handed Points', value='shortHandedPoints'),
                create_choice(name='Short Handed Time On Ice', value='shortHandedTimeOnIce'),
                create_choice(name='Blocked', value='blocked'),
                create_choice(name='Plus/Minus', value='plusMinus'),
                create_choice(name='Shifts', value='shifts')
            ]
        ), create_option(
            name="season",
            description="Changes the season that the stat value is pulled from. Defaults to current season.",
            option_type=3,
            required=False
        )
    ])
@client.command()
async def skaterSingleStat(ctx, playername, stat, season= botLogic.GetCurrentSeason()):
    await ctx.defer()
    player = hockeyPy.Player(playername, season)
    playername = player.GetPlayerName()
    statValue = player.stats[stat]
    statName = botLogic.statProperName(stat)
    if statValue == 1:
        lastChar = list(statName)[-1]
        statName = statName.replace(lastChar, '')
    formatSeason = season[:4] + '-' + season[4:]
    r, g, b = player.teamColour
    if isinstance(statValue, float):
        e = discord.Embed(
                        title= f'Single Stat | {playername}',
                        description= f'{statName} : {statValue}% | Season : {formatSeason}',
                        colour = discord.Colour.from_rgb(r, g, b))
        await ctx.reply('', embed= e)
    else:
        e = discord.Embed(
                title= f'Single Stat | {playername}',
                description= f'{statName} : {statValue} | Season : {formatSeason}',
                colour = discord.Colour.from_rgb(r, g, b))
        await ctx.reply('', embed= e)

@slash.slash(
    name="goaliesinglestat", 
    description="Provides the requested number of scoring leaders of the requested stat, for the requested team!", 
    options= [
        create_option(
            name="playername", 
            description="The name of the player. Format: CaleMakar. SabatianAho: Use SabatianAhoSWE or SabatianAhoFIN", 
            option_type=3, 
            required=True
        ), create_option(
            name="stat",
            description="Changes the stat that is returned." ,
            option_type=3,
            required=True,
            choices = [
                create_choice(name='Over Time Losses', value='ot'),
                create_choice(name='Shutouts', value='shutouts'),
                create_choice(name='Ties', value='ties'),
                create_choice(name='Wins', value='wins'),
                create_choice(name='Losses', value='losses'),
                create_choice(name='Saves', value='saves'),
                create_choice(name='Power Play Saves', value='powerPlaySaves'),
                create_choice(name='Short Handed Saves', value='shortHandedSaves'),
                create_choice(name='Even Saves', value='evenSaves'),
                create_choice(name='Short Handed Saves', value='shortHandedShots'),
                create_choice(name='Even Shots', value='evenShots'),
                create_choice(name='Power Play Shots', value='powerPlayShots'),
                create_choice(name='Save Percentage', value='savePercentage'),
                create_choice(name='Goals Againts Average', value='goalAgainstAverage'),
                create_choice(name='Games Started', value='gamesStarted'),
                create_choice(name='Shots Against', value='shotsAgainst'),
                create_choice(name='Goals Againts', value='goalsAgainst'),
                create_choice(name='Time On Ice Average', value='timeOnIcePerGame'),
                create_choice(name='Power Play Save Percentage', value='powerPlaySavePercentage'),
                create_choice(name='Short Handed Save Percentage', value='shortHandedSavePercentage'),
                create_choice(name='Even Strength Save Percentage', value='evenStrengthSavePercentage')
            ]
        ), create_option(
            name="season",
            description="Changes the season that the stat value is pulled from. Defaults to current season.",
            option_type=3,
            required=False
        )
    ])
@client.command()
async def GoalieSingleStat(ctx, playername, stat, season= botLogic.GetCurrentSeason()):
    await ctx.defer()
    player = hockeyPy.Player(playername, season)
    playername = player.GetPlayerName()
    statValue = player.stats[stat]
    statName = botLogic.statProperName(stat)
    if statValue == 1:
        lastChar = list(statName)[-1]
        statName = statName.replace(lastChar, '')
    formatSeason = season[:4] + '-' + season[4:]
    r, g, b = player.teamColour
    if isinstance(statValue, float):
        e = discord.Embed(
                        title= f'Single Stat | {playername}',
                        description= f'{statName} : {statValue}% | Season : {formatSeason}',
                        colour = discord.Colour.from_rgb(r, g, b))
        await ctx.reply('', embed= e)
    else:
        e = discord.Embed(
                title= f'Single Stat | {playername}',
                description= f'{statName} : {statValue} | Season : {formatSeason}',
                colour = discord.Colour.from_rgb(r, g, b))
        await ctx.reply('', embed= e)

@slash.slash(
    name="whatsnew", 
    description="Provides a quick rundown of the newest added features to the bot!",
    options=[])
@client.command()
async def whatsNew(ctx):
    with open('new.txt', 'r') as f:
        x = f.read()
    e = discord.Embed(title='New features/Changes', description=x, colour= discord.Colour.from_rgb(0,0,0))
    await ctx.reply('', embed= e)

@slash.slash(
    name="info", 
    description=" There is no shame in asking for help! Provides many sources to help with the bot.",
    options=[])
@client.command()
async def info(ctx):
    await ctx.reply('Visits the website, email me, or view my GitHub!\n\u2022 GitHub: https://github.com/Special-Sharpie/HockeyStatsBot \n\u2022 Website: https://hockeystatsbot.ca/ \n\u2022 Email: hockeystatsbot@gmail.com')

@slash.slash(
    name="donate", 
    description="If you enjoy the bot, consider supporting its development!.",
    options=[])
@client.command()
async def donate(ctx):
    await ctx.reply('Donate here: https://www.paypal.com/paypalme/hockeystatsbot')

#Runs the bot
with open('token.txt', 'r+') as f:
    token = f.read()
    client.run(token)