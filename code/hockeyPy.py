import json
import requests
import pprint as p

# This is a WIP file I am playing with. The intent is to simplify my interactions with the API, and accompanying data.
# I will be slowly reworking commands to pull from the classes defined here, opposed to the current methods used.

class Skater: # Designed to be a parent class, which the end user will inherite from
    def __init__(self, nameCode):
        self.nameCode = nameCode # Establishes which player is requested
        self.id = self.getPlayerID(self.nameCode)
        self.statsUrl = 'https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=statsSingleSeason&season=20202021'.format(self.id)
        self.infoUrl = 'https://statsapi.web.nhl.com/api/v1/people/{}'.format(self.id)
        self.stats = self.getStatsDict(self.statsUrl) # Returns a dictionary of the players stats
        self.info = self.getInfoDict(self.infoUrl) # Returns a dictionary of the players info

    def getPlayerID(self, PlayerName):
        with open('Player.json', 'r+') as f:
            data = json.load(f)
            return(data[PlayerName])
    
    def getInfoDict(self, url):
        request = requests.get(url)
        FullName = request.json()['people'][0]
        return FullName

    def getStatsDict(self, url):
        request = requests.get(url)
        stats = request.json()['stats'][0]['splits'][0]['stat']
        return stats

class Team: # Designed to be a parent class, which the end user will inherite from
    def __init__(self, teamABBR):
        self.abbr = teamABBR
        self.id = self.getTeamID(self.abbr)
        self.statsUrl = 'https://statsapi.web.nhl.com/api/v1/teams/{}/stats'.format(self.id)
        self.infoUrl = 'https://statsapi.web.nhl.com/api/v1/teams/{}'.format(self.id)
        self.stats = self.getStatsDict(self.statsUrl)
        self.ranks = self.getRanksDict(self.statsUrl)
        self.info = self.getInfoDict(self.infoUrl)
        self.colour = self.getTeamColour(self.id)
        
    def __add__(self, other): # Adding two Team instances together results in the comparison of their Win/Loss record
        return '{}: {} | {}: {}'.format(self.abbr, self.getWinLoss(), other.abbr, other.getWinLoss())

    def getTeamID(self, abbr):
        with open('ABBRid.json', 'r+') as f:
            data = json.load(f)
            return data[abbr]
    
    def getTeamColour(self, ID):
        with open('TeamColour.json', 'r+') as f:
            data = json.load(f)
            return data[ID]
    
    def getStatsDict(self, url):
        request = requests.get(url)
        stats = request.json()['stats'][0]['splits'][0]['stat']
        return stats

    def getRanksDict(self, url):
        request = requests.get(url)
        ranks = request.json()['stats'][1]['splits'][0]['stat']
        return ranks

    def getInfoDict(self, url):
        request = requests.get(url)
        info = request.json()['teams'][0]
        return info

    def getWinLoss(self):
        win = self.stats['wins']
        loss = self.stats['losses']
        ot = self.stats['ot']
        point = self.stats['pts']
        return '({}/{}/{}/{})'.format(win, loss, ot, point)
