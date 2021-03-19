import requests as r
import pprint as p
import botLogic as bot

def playerInfo(playerName):
    player = bot.GetPlayerID(playerName)
    url = 'https://statsapi.web.nhl.com/api/v1/people/{}'.format(player)
    data = r.get(url)
    playerInfo = data.json()['people'][0]
    name = playerInfo['fullName']
    birthCity = playerInfo['birthCity']
    try:
        birthStateProvince = playerInfo['birthStateProvince']
    except:
        birthStateProvince = 'N/A'
    birthCountry = playerInfo['birthCountry']
    height = playerInfo['height']
    weight = str(playerInfo['weight']) + ' lbs'
    age = playerInfo['currentAge']
    return 'Name: {}\nBirth City: {}\nBirth State/Province: {}\nBirth Country: {}\nAge: {}\nHeight: {}\nWeight: {}'.format(name, birthCity, birthStateProvince, birthCountry, age, height, weight)

def playerTeamInfo(playerName):
    player = bot.GetPlayerID(playerName)
    url = 'https://statsapi.web.nhl.com/api/v1/people/{}'.format(player)
    data = r.get(url)
    playerInfo = data.json()['people'][0]
    altCapt = playerInfo['alternateCaptain']
    capt = playerInfo['captain']
    team = playerInfo['currentTeam']['name']
    number = playerInfo['primaryNumber']
    position = playerInfo['primaryPosition']['name']
    roster = playerInfo['rosterStatus']
    rookie = playerInfo['rookie']
    dominantHand = playerInfo['shootsCatches']
    if dominantHand == 'L':
        dominantHand = 'Left'
    elif dominantHand == 'R':
        dominantHand == 'Right'
    return 'Team: {}\nPosition: {}\nJersey Number: {}\nCaptain: {}\nAlt. Captain: {}\nOn Roster: {}\nRookie: {}\nShoots/Catches: {}'.format(team, position, number, capt, altCapt, roster, rookie, dominantHand)
