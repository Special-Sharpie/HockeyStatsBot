import json
import requests


def WinLossTeam(ID):
    ls = []
    statsurl = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + str(ID) + '/stats')
    name = statsurl.json()['stats'][0]['splits'][0]['team']['name']
    gamesPlayed = statsurl.json()['stats'][0]['splits'][0]['stat']['gamesPlayed']
    wins = statsurl.json()['stats'][0]['splits'][0]['stat']['wins']
    losses = statsurl.json()['stats'][0]['splits'][0]['stat']['losses']
    otlosses = statsurl.json()['stats'][0]['splits'][0]['stat']['ot']
    points = statsurl.json()['stats'][0]['splits'][0]['stat']['pts']
    ls.extend((name, gamesPlayed, wins, losses, otlosses, points))
    return ls