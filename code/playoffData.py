import requests
import pprint
import json


def getWinner(url):
    team1win = url.json()['rounds'][-1]['series'][0]['matchupTeams'][0]['seriesRecord']['wins']
    team1loss = url.json()['rounds'][-1]['series'][0]['matchupTeams'][0]['seriesRecord']['losses']
    if team1win - team1loss  < 0 :
        return 1
    else:
        return 0
def getID(url):
    x = getWinner(url)
    if x == 1:
        teamID = url.json()['rounds'][-1]['series'][0]['matchupTeams'][1]['team']['id']
        return teamID
    else:
        teamID = url.json()['rounds'][-1]['series'][0]['matchupTeams'][0]['team']['id']
        return teamID

def playoffWin(season):
    ls = []
    url = requests.get('https://statsapi.web.nhl.com/api/v1/tournaments/playoffs?expand=round.series,schedule.game.seriesSummary&season=' + str(season))
    teamID = getID(url)
    series = url.json()['rounds']
    stanleyCup = url.json()['rounds'][len(series) - 1]['names']['name']
    data = url.json()['rounds'][len(series) - 1]['series'][0]['matchupTeams'][getWinner(url)]
    #pprint.pprint(data)
    teamName = data['team']['name']
    wins = data['seriesRecord']['wins']
    loss = data['seriesRecord']['losses']
    ls.extend((str(season)[4:], stanleyCup, teamName, str(wins), str(loss), str(teamID)))
    return ls



playoffWin('20182019')