import discord
from discord.ext import commands
import requests
import datetime
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


#Variables
client = commands.Bot(command_prefix='HS-')
game = discord.Game("Prefix is now HS-")

#Events:
@client.event
async def on_ready():
    print('The world is calling {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_command_error(ctx, error):
    #Error Handling!
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
@client.command()
async def serverCount(ctx):
    await ctx.channel.send('Currently providing hockey stats to {} servers!'.format(client.guilds))

@client.event
async def on_guild_join(ctx):
    guildID = ctx.id
    botLogic.writeJSON('ServerTimezone.json', guildID, 'MT')

#Commands

@client.command()
@commands.has_permissions(administrator=True)
async def setTimezone(ctx, TZ):
    if TZ == 'MT' or TZ == 'PT' or TZ == 'CT' or TZ == 'ET':
        guildID = ctx.message.guild.id
        botLogic.writeJSON('ServerTimezone.json', guildID, TZ)
        await ctx.channel.send('Timezone set to {}'.format(TZ))
    else:
        await ctx.channel.send('Yeah that timezone is far to complex for my small brained creator.')
@client.command()
async def skaterCareer(ctx, player):
    playerID = botLogic.readJSON('Player.json', player)
    playerName = botLogic.GetPlayerName(playerID)
    x = Career.skaterStats(str(playerID))
    if len(x[1]) < 1024:
        e = discord.Embed(title="Career Stats - {}".format(playerName))
        e.add_field(name=x[0], value= x[1])
        e.set_footer(text=x[2])
        await ctx.channel.send('', embed= e)
    else:
        await  ctx.channel.send('Career Stats - {}\n'.format(playerName) + x[0] +'\n' + x[1] + '\n' + x[2])

@client.command()
async def teamWL(ctx, ABBR):
    ID = botLogic.readJSON('ABBRid.json', ABBR)
    y = botLogic.readJSON('TeamColour.json', ID)
    season = botLogic.GetCurrentSeason()
    x = teamWinLoss.WinLossTeam(ID)
    e = discord.Embed(title= 'Single Season Win/Loss!', description= 'The ' + season[:4] + '-' + season[4:] +' Win/Loss record for the ' + x[0], colour= discord.Colour.from_rgb(y[0], y[1], y[2]))
    e.add_field(name= 'Record:', value= str(x[2]) + '/' + str(x[3]) + '/' + str(x[4]) + ' in ' + str(x[1]) + ' games, tallying ' + str(x[5]) + ' points.')
    await ctx.channel.send('', embed= e)

@client.command()
async def currentSeason(ctx):
    x = botLogic.GetCurrentSeason()
    await ctx.channel.send("Its currently the {}-{} season".format(x[:4], x[4:]))

@client.command()
async def teamID(ctx):
    with open('TeamID.txt', 'r') as f:
        x = f.read()
        await ctx.author.send(x)

@client.command()
async def lifeWL(ctx, ABBR1, ABBR2):
    FranID1 = botLogic.readJSON('ABBRid.json', ABBR1)
    FranID2 = botLogic.readJSON('ABBRid.json', ABBR2)
    r, g, b = botLogic.readJSON('TeamColour.json', FranID1)
    x = winloss.winloss(FranID1, FranID2)
    e = discord.Embed(title= 'Life Time Win/loss!', description= 'The lifetime Win/Loss/OT/T \n' + x[0] + ' VS. ' + x[1], colour= discord.Colour.from_rgb(r, g, b))
    e.add_field(name= 'Home Record:', value= str(x[2]) + '/' + str(x[3]) + '/' + str(x[4]) + '/' + str(x[5]), inline= False)
    e.add_field(name= 'Road Record:', value= str(x[6]) + '/' + str(x[7]) + '/' + str(x[8]) + '/' + str(x[9]), inline= False)
    e.add_field(name= 'Total Record:', value= str(x[10]) + '/' + str(x[11]) + '/' + str(x[12]) + '/' + str(x[13]), inline= False)
    await ctx.channel.send('', embed= e)


@client.command()
async def Pstats(ctx, PlayerName, playoff= 'R', season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
    if playoff == "R":
        x = playerStats.stats(playerID, playoff, season)
        e = discord.Embed(title= 'Single Season Stats - ' + season[:4] +'-'+ season[4:], description= 'Stats for ' + x[0], colour= discord.Colour.from_rgb(0,0,0))
        e.add_field(name='Stats:', value= x[1], inline= False)
        await ctx.channel.send('', embed= e)
    elif playoff == 'P':
        x = playerStats.stats(playerID, playoff, season)
        e = discord.Embed(title= 'Post Season Stats - ' + season[4:] + ' Stanley Cup Playoffs', description= 'Stats for ' + x[0], colour= discord.Colour.from_rgb(0,0,0))
        e.add_field(name='Stats:', value= x[1], inline= False)
        await ctx.channel.send('', embed= e)

@client.command()
async def perGame(ctx, player, stat, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', player)
    playerName = botLogic.GetPlayerName(playerID)
    statName, statAvg, rawStat, games = statsPerGame.statsPerGameCalculator(playerID, stat, season)
    e = discord.Embed(
                    title= '{} Per Game - {}'.format(statName, playerName),
                    description='{} per Game: {} \n Total {}: {}\nTotal Games: {}'.format(statName, statAvg, statName, rawStat, games),
                    colour= discord.Colour.from_rgb(0,0,0)
                    )
    await ctx.channel.send('', embed=e)

#Commands for individual PLayer/Goalie Stats

#Goalies:
@client.command()
async def Gotl(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
    stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
    goalieOT = stats_url.json()['stats'][0]['splits'][0]['stat']['ot']
    if season == botLogic.GetCurrentSeason():
        e = discord.Embed(title= 'Wins - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' has lost ' + str(goalieOT) + ' games in Overtime so far this season!',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
    else:
        e = discord.Embed(title= 'Wins - ' + botLogic.GetPlayerName(playerID) +' - '+ season[:4] + '-' + season[4:],
                         description=botLogic.GetPlayerName(playerID) + ' lost ' + str(goalieOT) + ' games in Overtime during the ' + season[:4] + '-' + season[4:] + ' season',
                          colour=discord.Colour.from_rgb(0, 0, 0))
        await ctx.channel.send('', embed= e)
@client.command()
async def Gwins(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Gloss(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Gsaves(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Gtoi(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Gshutout(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Gsavep(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Ggaa(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Ggames(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Gshota(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Ggoala(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pgoals(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Passists(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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

@client.command()#20
async def Ppoints(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pshots(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pplusminus(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Ptoi(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pgplayed(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pppgoals(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Ppppoints(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pgwgoals(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Ppenalty(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Phits(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pbshots(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Potgoals(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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
async def Pshgoals(ctx, PlayerName, season= botLogic.GetCurrentSeason()):
    playerID = botLogic.readJSON('Player.json', PlayerName)
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

@client.command()
async def Gnext(ctx, ABBR):
    guildID = ctx.message.guild.id
    teamID = botLogic.readJSON('ABBRid.json', ABBR)
    r, g, b = botLogic.readJSON('TeamColour.json', teamID)
    TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
    x = next.next(teamID, TZ)
    e = discord.Embed(title= 'Next Game!', description= x, colour= discord.Colour.from_rgb(r, g, b))
    #e.set_footer(text= 'Times are in Mountain, + 1 Pacific Time, -2 Eastern Time')
    await ctx.channel.send('', embed= e)

@client.command()
async def next7(ctx, ABBR):
    guildID = ctx.message.guild.id
    ID = botLogic.readJSON('ABBRid.json', ABBR)
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
    await ctx.channel.send('', embed=e)

@client.command()
async def Glast(ctx, ABBR):
    teamID = botLogic.readJSON('ABBRid.json', ABBR)
    r, g, b = botLogic.readJSON('TeamColour.json', teamID)
    x = last.last(teamID)
    if len(x) == 1:
        e = discord.Embed(title= 'Last Game Played!', description= x[0], colour= discord.Colour.from_rgb(r, g, b))
        await ctx.channel.send('', embed=e)
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
    await ctx.channel.send('', embed= e)

@client.command()
async def Gtoday(ctx, ABBR):
    ID = botLogic.readJSON('ABBRid.json', ABBR)
    guildID = ctx.message.guild.id
    TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
    r, g, b = botLogic.readJSON('TeamColour.json', ID)
    x = gameDay.gday(ID, TZ)
    if x[0] < '3':
        e = discord.Embed(title= 'Game Day!', description= x[1] + ' VS. ' + x[2] + ' at ' + x[3], colour= discord.Colour.from_rgb(r, g, b))
        await ctx.channel.send('', embed= e)
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
        await ctx.channel.send('', embed=e)
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
        await ctx.channel.send('', embed=e)

@client.command()
async def divStandings(ctx, div):
    x = standings.div(div)
    e = discord.Embed(title= x[0][:4] + '-' + x[0][4:] +' '+ div + ' | Division Standings', description= x[1], colour= discord.Colour.from_rgb(0, 0, 0))
    await ctx.channel.send('', embed= e)

@client.command()
async def confStandings(ctx, conf):
    #x = standings.conf(conf)
    #e = discord.Embed(title= x[0][:4] + '-' + x[0][4:] +' '+ conf + ' Conference Standings', description= x[1], colour= discord.Colour.from_rgb(0, 0, 0))
    await ctx.channel.send('Conferences are not being used this season! We are witnessing history.')
@client.command()
async def leagueStandings(ctx, season= botLogic.GetCurrentSeason()):
    x = standings.league(season)
    e = discord.Embed(title= x[0][:4] + '-' + x[0][4:] + ' | League Standings', description= x[1], colour= discord.Colour.from_rgb(0, 0, 0))
    await ctx.channel.send('', embed= e)

@client.command()
async def SCFwinner(ctx, season):
    x = playoffData.playoffWin(season)
    r, g, b = botLogic.readJSON('TeamColour.json', x[5])
    e = discord.Embed(title= x[0] + ' ' + x[1], colour= discord.Colour.from_rgb(r, g, b))
    e.add_field(name= 'Champion:', value= 'The ' + x[2] + ' won the Stanley Cup', inline= False)
    e.add_field(name= 'Series Record:', value= x[3] + ' Wins, ' + x[4] + ' Losses', inline= True)
    await ctx.channel.send('', embed= e)

@client.command()
async def playoffStandings(ctx, abbr, round, season):
    x = playoffBracket.playoffStanding(abbr, round, season)
    r, g, b = botLogic.readJSON('TeamColour.json', x[6])
    e = discord.Embed(title =  x[0][4:] + ' Playoffs - ' + x[1], colour= discord.Colour.from_rgb(r, g, b))
    e.add_field(name = 'Match Up:', value = x[2] + ' VS. ' + x[3], inline= False)
    e.add_field(name = 'Series Record:', value = x[2] + ': ' + str(x[4]) + ' ' + x[3] + ': ' + str(x[5]), inline = True)
    await ctx.channel.send('', embed = e)

@client.command()
async def daySummary(ctx, RequestDate= str(datetime.date.today())):
    guildID = ctx.message.guild.id
    x = daySummery.daySumDate(RequestDate)
    date = x[1]
    TZ = botLogic.readJSON('ServerTimezone.json', str(guildID))
    e = discord.Embed(title= 'Day Summary - ' + date, colour= discord.Colour.from_rgb(0,0,0))
    i = 0
    while i < x[0]:
        z = daySummery.daySum(i, TZ, RequestDate)
        if len(z) == 7:
            e.add_field(name= z[0] + ' VS. ' + z[1], value= z[2] +': '+ str(z[4]) + ' | ' + z[3] + ': ' + str(z[5]) + ' | ' + z[6], inline= False)
        else:
            e.add_field(name= z[0] + ' VS. ' + z[1], value=z[2] + ' VS. ' + z[3] + ' | ' + z[4], inline=False)
        i += 1
    await ctx.channel.send('', embed= e)

@client.command()
async def draftByYear(ctx, team, year= 2020):
    teamID = botLogic.readJSON('ABBRid.json', team)
    teamFullName = botLogic.GetTeamName(teamID)
    r, g, b = botLogic.readJSON('TeamColour.json', teamID)
    results = DraftYear.draft(year, teamID)
    e = discord.Embed(title='{} Draft | {}'.format(year, teamFullName), colour= discord.Colour.from_rgb(r, g, b))
    for res in results:
        for draftee in results[res]:
            e.add_field(name=res, value=draftee, inline= False)
    await ctx.channel.send('', embed=e)

@client.command()
async def Pinfo(ctx, playerName):
    playerID = botLogic.GetPlayerID(playerName)
    fullName = botLogic.GetPlayerName(playerID)
    personal = playerInfo.playerInfo(playerName)
    teamBased = playerInfo.playerTeamInfo(playerName)
    e = discord.Embed(title='Player Info | {}'.format(fullName), colour=discord.Colour.from_rgb(0,0,0))
    e.add_field(name='Personal', value=personal)
    e.add_field(name='Team Based', value=teamBased)
    await ctx.channel.send('', embed=e)

@client.command()
async def whatsNew(ctx):
    with open('new.txt', 'r') as f:
        x = f.read()
    e = discord.Embed(title='New features/Changes', description=x, colour= discord.Colour.from_rgb(0,0,0))
    await ctx.author.send('', embed= e)

@client.command()
async def info(ctx):
    await ctx.author.send('A helpful document!', file= discord.File('HockeyBot_documentation.docx'))

#Runs the bot
with open('token.txt', 'r+') as f:
    token = f.read()
    client.run(token)