import json
import requests as r
import pprint as p
import botLogic as bot

statCodes = {
    "TOI" : ["timeOnIce", "Time On Ice", True],
    "A" : ["assists", "Assists", False],
    "G" : ["goals", "Goals", False],
    "PIM" : ["pim", "Penalty Minutes", False],
    "SHOTS" : ["shots", "Shots", False],
    "HITS" : ["hits", "Hits", False],
    "PPG" : ["powerPlayGoals", "Power Play Goals", False],
    "PPP" : ["powerPlayPoints", "Power Play Points", False],
    "PPTOI" : ["powerPlayTimeOnIce", "Power Play Time On Ice", True],
    "ETOI" : ["evenTimeOnIce", "Even Time On Ice", True],
    "SHTP" : ["shotPct", "Shot Percentage", False],
    "GWG" : ["gameWinningGoals", "Game Winning Goals", False],
    "OTG" : ["overTimeGoals", "Over Time Goals", False],
    "SHG" : ["shortHandedGoals", "Short Handed Goals", False],
    "SHP" : ["shortHandedPoints", "Short Handed Points", False],
    "SHTOI" : ["shortHandedTimeOnIce", "Short Handed Time On Ice", True],
    "B" : ["blocked", "Shots Blocked", False],
    "PM" : ["plusMinus", "Plus Minus", False],
    "P" : ["points", "Points", False],
    "SHIFTS" : ["shifts", "Shifts", False]
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

