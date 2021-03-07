import json
import requests
import botLogic


def div(div):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/standings')
    teamCount = url.json()['records'][botLogic.getDIVindex(div)]['teamRecords']
    season = botLogic.GetCurrentSeason()
    ls = []
    divIDs = []
    divRanks = []
    loss = []
    win = []
    ot = []
    points = []
    i = 0
    while i < len(teamCount):
        indexPos =teamCount[i]['team']['name']
        divRank = teamCount[i]['divisionRank']
        teamLoss = teamCount[i]['leagueRecord']['losses']
        teamWin = teamCount[i]['leagueRecord']['wins']
        teamOT = teamCount[i]['leagueRecord']['ot']
        teamPoints = teamCount[i]['points']
        divIDs.append(indexPos)
        divRanks.append(divRank)
        loss.append(teamLoss)
        win.append(teamWin)
        ot.append(teamOT)
        points.append(teamPoints)
        i += 1
    with open('rank.txt', 'w') as f:
        j = 0
        while j < len(teamCount):
            x = (str(divRanks[j]) + '. ' + str(divIDs[j]) + ' (' + str(win[j]) + '/' + str(loss[j]) + '/' + str(ot[j]) + '/' + str(points[j]) + ')')
            f.write(x + '\n')
            j += 1

    with open('rank.txt', 'r+') as f:
        LeaguesStats = f.read()
        ls.append(season)
        ls.append(LeaguesStats)
        f.truncate(0)
        return ls



def conf(conf):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/standings/byConference')
    season = botLogic.GetCurrentSeason()
    ls = []
    confRank = []
    teamName = []
    loss = []
    win = []
    ot = []
    points = []
    confStandings = url.json()['records'][botLogic.getConf(conf)]['teamRecords']
    i = 0
    while i < len(confStandings):
        rank = confStandings[i]['conferenceRank']
        name = confStandings[i]['team']['name']
        losss = confStandings[i]['leagueRecord']['losses']
        wins = confStandings[i]['leagueRecord']['wins']
        ots = confStandings[i]['leagueRecord']['ot']
        pointss = confStandings[i]['points']
        confRank.append(str(rank))
        teamName.append(name)
        win.append(str(wins))
        loss.append(str(losss))
        ot.append(str(ots))
        points.append(str(pointss))
        i += 1
    with open('rank.txt', 'w') as f:
        j = 0
        while j < len(confStandings):
            x = (str(confRank[j]) + '. ' + str(teamName[j]) + ' (' + str(win[j]) + '/' + str(loss[j]) + '/' + str(ot[j]) + '/' + str(points[j]) + ')')
            f.write(x + '\n')
            j += 1

    with open('rank.txt', 'r+') as f:
        LeaguesStats = f.read()
        ls.append(season)
        ls.append(LeaguesStats)
        f.truncate(0)
        return ls




def league(season):
    url = requests.get('https://statsapi.web.nhl.com/api/v1/standings/byLeague?season=' + str(season))
    teamName = []
    leagueRank = []
    loss = []
    win = []
    ot = []
    points = []
    ls = []
    records = url.json()['records'][0]['teamRecords']
    if botLogic.isTies(str(season)) == False:
        i = 0
        while i < len(records):
            Name = records[i]['team']['name']
            Rank = records[i]['leagueRank']
            teamWIN = records[i]['leagueRecord']['wins']
            teamLOSS = records[i]['leagueRecord']['losses']
            teamOT = records[i]['leagueRecord']['ot']
            teamPOINTS = records[i]['points']
            teamName.append(Name)
            leagueRank.append(Rank)
            win.append(str(teamWIN))
            loss.append(str(teamLOSS))
            ot.append(str(teamOT))
            points.append(str(teamPOINTS))
            i += 1
        j = 0
        with open('rank.txt', 'w')as f:
            while j < len(records):
                x = leagueRank[j] + '. ' + teamName[j] + ' (' + win[j] + '/' + loss[j] + '/' + ot[j] + '/' + points[j] + ')'
                f.write(x + '\n')
                j += 1

    elif botLogic.isTies(str(season)) == True:
        i = 0
        while i < len(records):
            Name = records[i]['team']['name']
            Rank = records[i]['leagueRank']
            teamWIN = records[i]['leagueRecord']['wins']
            teamLOSS = records[i]['leagueRecord']['losses']
            teamTIES = records[i]['leagueRecord']['ties']
            teamPOINTS = records[i]['points']
            teamName.append(Name)
            leagueRank.append(Rank)
            win.append(str(teamWIN))
            loss.append(str(teamLOSS))
            ot.append(str(teamTIES))
            points.append(str(teamPOINTS))
            i += 1
            j = 0
        with open('rank.txt', 'w')as f:
            while j < len(records):
                x = leagueRank[j] + '. ' + teamName[j] + ' (' + win[j] + '/' + loss[j] + '/' + ot[j] + '/' + points[j] + ')'
                f.write(x + '\n')
                j += 1

    with open('rank.txt', 'r+') as f:
        LeaguesStats = f.read()
        ls.append(season)
        ls.append(LeaguesStats)
        f.truncate(0)
        return ls



