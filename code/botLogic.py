import random
import requests
import datetime
from datetime import timedelta
import pytz
import time
import json

# Functions that control the bots logic
def writeJSON(file, key, value):
    with open(file, 'r+') as f:
        data = json.load(f)
        data[key] = value
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

def readJSON(file, value):
    with open(file, 'r+') as f:
        data = json.load(f)
        return data[value]

def clearJSON(file, deletedValue):
    with open(file, "r+")as f:
        data = json.load(f)
        del data[deletedValue]
        f.seek(0)
        json.dumps(data)
        f.truncate()

def statProperName(code):
    codes = {
        'ot' : 'Over Time Losses',
        'shutouts' : 'Shutouts',
        'ties' : 'Ties',
        'wins' : 'Wins',
        'losses' : 'Losses',
        'saves' : 'Saves',
        'powerPlaySaves' : 'Power Play Saves',
        'shortHandedSaves' : 'Short Handed Saves',
        'evenSaves' : 'Even Saves',
        'shortHandedShots' : 'Short Handed Saves',
        'evenShots' : 'Even Shots',
        'powerPlayShots' : 'Power Play Shots',
        'savePercentage' : 'Save Percentage',
        'goalAgainstAverage' : 'Goals Againts Average',
        'gamesStarted' : 'Games Started',
        'shotsAgainst' : 'Shots Against',
        'goalsAgainst' : 'Goals Againts',
        'timeOnIcePerGame' : 'Time On Ice Average',
        'powerPlaySavePercentage' : 'Power Play Save Percentage',
        'shortHandedSavePercentage' : 'Short Handed Save Percentage',
        'evenStrengthSavePercentage' : 'Even Strength Save Percentage',
        'timeOnIce' : 'Time On Ice',
        'assists' : 'Assists',
        'goals' : 'Goals',
        'pim' : 'Penalty Infraction Minutes',
        'shots' : 'Shots',
        'games' : 'Games Played',
        'hits' : 'Hits',
        'powerPlayGoals' : 'Power Play Goals',
        'powerPlayPoints' : 'Power Play Points',
        'powerPlayTimeOnIce' : 'Power Play Time On Ice',
        'evenTimeOnIce' : 'Even Time On Ice',
        'penaltyMinutes' : 'Penalty Minutes',
        'faceOffPct' : 'Faceoff Percentage',
        'shotPct' : 'Shot Percentage',
        'gameWinningGoals' : 'Game Winning Goals',
        'overTimeGoals' : 'Overtime Goals',
        'shortHandedGoals' : 'Short Handed Goals',
        'shortHandedPoints' : 'Short Handed Points',
        'shortHandedTimeOnIce' : 'Short Handed Time On Ice',
        'blocked' : 'Blocked',
        'plusMinus' : 'Plus/Minus',
        'points' : 'Points',
        'shifts' : 'Shifts'
    }
    return codes[code]

def Chadthing():
    y = random.randint(1, 9)
    if y <= 2:
        return 'tier1'
    if 4 >= y > 2:
        return 'tier2'
    if 7 >= y > 4:
        return 'tier3'
    if y > 7:
        return 'tier4'

def addToDatabase(MemberID, tier):
    with open('ChadDataBase.json', 'r+') as f:
        data = json.load(f)
        data[MemberID] = tier
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def GetPlayerID(PlayerName):
    with open('AllTimePlayer.json', 'r+') as f:
        data = json.load(f)
        return(data[PlayerName])

def GetCurrentSeason():
    season_url = requests.get('https://statsapi.web.nhl.com/api/v1/seasons/current')
    currentSeason = season_url.json()['seasons'][0]['seasonId']
    return currentSeason

def GetPlayerName(playerID):
    name_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID))
    FullName = name_url.json()['people'][0]['fullName']
    return FullName

def CheckIfRun(ID):
    with open('ChadDataBase.json', 'r+') as f:
        data = json.load(f)
        return(data[ID])

def findOppIndex(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i

def getDIVindex(div):
    if div == 'Central':
        return 0
    if div == 'East':
        return 1
    if div == 'North':
        return 2
    if div == 'West':
        return 3

def getConf(conf):
    if conf == 'Eastern':
        return 0
    if conf == 'Western':
        return 1

def isTies(season):
    tiesUrl =  requests.get('https://statsapi.web.nhl.com/api/v1/seasons/' + season)
    ties = tiesUrl.json()['seasons'][0]['tiesInUse']
    if ties:
        return True
    else:
        return False

def homeOrAway(url, ID):
    check = url.json()['dates'][0]['games'][0]['teams']
    away = check['away']['team']['id']
    home = check['home']['team']['id']
    if ID == str(home):
        return 'home'
    elif ID == str(away):
        return 'away'

def GetOppTeam(HomeOrAway):
    if HomeOrAway == 'home':
        return 'away'
    if HomeOrAway == 'away':
        return 'home'

def GetTeamName(ID):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + str(ID))
    name = url.json()['teams'][0]['name']
    return name

def getRound(round, season):
    season = season
    round = round
    if season == '20192020':
        if round == 'SCQ':
            return 0
        if round == 'R1':
            return 1
        if round == 'R2':
            return 2
        if round == 'CF':
            return 3
        if round == 'SCF':
            return 4
    else:
        if round == 'R1':
            return 0
        if round == 'R2':
            return 1
        if round == 'CF':
            return 2
        if round == 'SCF':
            return 3

def getIndex(url, abbr, round, season):
    season = season
    round = round
    data = url.json()['rounds'][getRound(round, season)]['series']
    i = 0

    while i < len(data):
        if data[i]['names']['teamAbbreviationA'] == abbr:
            return i
            break
        elif data[i]['names']['teamAbbreviationB'] == abbr:
            return i
            break
        else:
            i += 1

def getLeader(url, abbr, round, season):
    season = season
    round = round
    team1win = url.json()['rounds'][getRound(round, season)]['series'][getIndex(url, abbr, round, season)]['matchupTeams'][0]['seriesRecord']['wins']
    team1loss = url.json()['rounds'][getRound(round, season)]['series'][getIndex(url, abbr, round, season)]['matchupTeams'][0]['seriesRecord']['losses']
    if team1win > team1loss:
        return 0
    elif team1win < team1loss:
        return 1
    elif team1win == team1loss:
        return 0

def getLosser(url, abbr, round, season):
    season = season
    round = round
    if getLeader(url, abbr, round, season) == 0:
        return 1
    if getLeader(url, abbr, round, season) == 1:
        return 0

def getActualRoundName(url, round, season):
    season = season
    round = round
    actualRound = url.json()['rounds'][getRound(round, season)]['names']['name']
    return actualRound

def getGamePK(team):
    date = datetime.datetime.now(pytz.timezone('Canada/Mountain')).date()
    url = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team) + '&startDate=' + str(date) +'&endDate=' + str(date))
    pk = url.json()['dates'][0]['games'][0]['gamePk']
    return str(pk)

def getPastPk(team, date):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(team) + '&startDate=' + str(date) +'&endDate=' + str(date))
    pk = url.json()['dates'][0]['games'][0]['gamePk']
    return str(pk)

def getOtherAbbr(otherId):
    with open('ABBRid.json', 'r+') as f:
        x = f.read()
        data = json.loads(x)
        return ((list(data.keys())[list(data.values()).index(otherId)]))

def gameStats(team):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/game/' + getGamePK(team) + '/boxscore')
    awayStats = url.json()['teams']['away']['teamStats']['teamSkaterStats']
    homeStats =url.json()['teams']['home']['teamStats']['teamSkaterStats']
    x = list(awayStats.values())
    y = list(homeStats.values())
    z = x + y
    return z

def pastGameStats(team, date):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/game/' + getPastPk(team, date) + '/boxscore')
    awayStats = url.json()['teams']['away']['teamStats']['teamSkaterStats']
    homeStats =url.json()['teams']['home']['teamStats']['teamSkaterStats']
    x = list(awayStats.values())
    y = list(homeStats.values())
    z = x + y
    return z

def getGoalScorers(team, date):
    ls = []
    pk = getPastPk(team, date)
    url = requests.get('https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(pk))
    playLength = url.json()['liveData']['plays']['allPlays']
    i = 0
    while i < len(playLength):
        event = url.json()['liveData']['plays']['allPlays'][i]['result']['event']
        if event == 'Goal':
            team = url.json()['liveData']['plays']['allPlays'][i]['team']['triCode']
            desc = url.json()['liveData']['plays']['allPlays'][i]['result']['description']
            period = url.json()['liveData']['plays']['allPlays'][i]['about']['period']
            time = url.json()['liveData']['plays']['allPlays'][i]['about']['periodTime']
            goal ='{}: {} Period: {} Time: {}'.format(team, desc, period, time)
            ls.append(goal)
        i += 1
    return ls

def getGameTime(teamID, date):
    ls = []
    pk = getPastPk(teamID, date)
    url = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(pk)
    url = requests.get(url)
    time = url.json()['liveData']['linescore']['currentPeriodTimeRemaining']
    period = url.json()['liveData']['linescore']['currentPeriodOrdinal']
    ls.extend((time, period))
    return ls

def getPlayerType(playerID):
    request = requests.get(f'https://statsapi.web.nhl.com/api/v1/people/{playerID}')
    postion = request.json()['people'][0]['primaryPosition']['code']
    if postion == 'G':
        return True
    else:
        return False

