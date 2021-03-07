import json
import requests
import pprint
import datetime
import pytz
import botLogic


def playoffStanding(abbr, round, season):
    ls = []
    url = requests.get('https://statsapi.web.nhl.com/api/v1/tournaments/playoffs?expand=round.series,schedule.game.seriesSummary&season=' + season)
    roundFormat = url.json()['rounds'][0]['format']['description']
    index = botLogic.getLeader(url, abbr, round, season)
    index2 = botLogic.getLosser(url, abbr, round, season)
    data = url.json()['rounds'][botLogic.getRound(round, season)]['series'][botLogic.getIndex(url, abbr, round, season)]['matchupTeams']
    wins = data[index]['seriesRecord']['wins']
    loss = data[index]['seriesRecord']['losses']
    name = data[index]['team']['name']
    teamID = data[index]['team']['id']
    name2 = data[index2]['team']['name']
    roundName = botLogic.getActualRoundName(url, round, season)

    ls.append(season)
    ls.append(roundName)
    ls.append(name)
    ls.append(name2)
    ls.append(wins)
    ls.append(loss)
    ls.append(str(teamID))
    ls.append(roundFormat)
    return ls

#playoffStanding(abbr, round, season)
