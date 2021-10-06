import json
import requests as r
import pprint as p
import botLogic as bot

statCodes = {
    "timeOnIce" : ["timeOnIce", "Time On Ice", True],
    "assists" : ["assists", "Assists", False],
    "goals" : ["goals", "Goals", False],
    "pim" : ["pim", "Penalty Minutes", False],
    "shots" : ["shots", "Shots", False],
    "hits" : ["hits", "Hits", False],
    "powerPlayGoals" : ["powerPlayGoals", "Power Play Goals", False],
    "powerPlayPoints" : ["powerPlayPoints", "Power Play Points", False],
    "powerPlayTimeOnIce" : ["powerPlayTimeOnIce", "Power Play Time On Ice", True],
    "evenTimeOnIce" : ["evenTimeOnIce", "Even Time On Ice", True],
    "shotPct" : ["shotPct", "Shot Percentage", False],
    "gameWinningGoals" : ["gameWinningGoals", "Game Winning Goals", False],
    "overTimeGoals" : ["overTimeGoals", "Over Time Goals", False],
    "shortHandedGoals" : ["shortHandedGoals", "Short Handed Goals", False],
    "shortHandedPoints" : ["shortHandedPoints", "Short Handed Points", False],
    "shortHandedTimeOnIce" : ["shortHandedTimeOnIce", "Short Handed Time On Ice", True],
    "blocked" : ["blocked", "Shots Blocked", False],
    "plusMinus" : ["plusMinus", "Plus Minus", False],
    "points" : ["points", "Points", False],
    "shifts" : ["shifts", "Shifts", False]
}

def findColon(time):
    ls = list(time)
    for i in ls:
        if i == ':':
            return ls.index(i)

def avgTime(time, games):
    newtime = (int(time[:findColon(time)]) * 60 + int(time[(findColon(time) + 1):]))
    avgtime = newtime//games
    x = avgtime//60
    y = x*60
    z = avgtime - y
    if z < 10:
        z = '0' + str(z)
        return str(x) +':'+ str(z)
    else:
        return str(x) + ':' + str(z)

def avgShotPer(response):
    goals = response['goals']
    shots = response['shots']
    games = response['games']
    return (goals/games) / (shots/games)

def statsPerGameCalculator(player, requestedStat, season= bot.GetCurrentSeason()):
    ls = []
    url = 'https://statsapi.web.nhl.com/api/v1/people/' + str(player) + '/stats?stats=statsSingleSeason&season=' + str(
         season)
    statCode, statName, isTime = statCodes[requestedStat]
    stats_request = r.get(url)
    stats = stats_request.json()['stats'][0]['splits'][0]['stat']
    games = stats['games']
    stat = stats[statCode]
    if isTime:
        avg = avgTime(stat, games)
        ls.extend((statName, avg, stat, games))
        return ls
    elif requestedStat == 'SHTP':
        avg = "{:.2f}".format(avgShotPer(stats))
        ls.extend((statName, avg, stat, games))
        return ls
    else:
        avg = "{:.2f}".format(stat/games)
        ls.extend((statName, avg, stat, games))
        return ls

