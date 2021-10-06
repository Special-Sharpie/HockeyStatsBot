import json
import requests
import pprint as p

# This is a WIP file I am playing with. The intent is to simplify my interactions with the API, and accompanying data.
# I will be slowly reworking commands to pull from the classes defined here, opposed to the current methods used.

def GetCurrentSeason():
    season_url = requests.get('https://statsapi.web.nhl.com/api/v1/seasons/current')
    currentSeason = season_url.json()['seasons'][0]['seasonId']
    return currentSeason

class DateError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class TeamError(Exception):
    def __init__(self, errorCode):
        self.errors = {
            'InvalidStatCode': 'Stat code requested is unsupported, review <Player Class>.stats for all valid codes.',
            'InvalidTeamAbbr': 'Provided team abbrevaiton failed to return a valid team ID.'
        }
        super().__init__(self.errors[errorCode])

class PeriodError(Exception):
    def __init__(self, errorCode):
        self.errors =  {
            'NegValue': "Invaid Period Number; Value must be greater or equal tho 0.",
            'ValueOutOfRange' : 'Period Number Out Of Range'
        }
        super().__init__(self.errors[errorCode])

class Player: # Designed to be a parent class, which the end user will inherite from
    def __init__(self, nameCode, season = GetCurrentSeason()):
        self.nameCode = nameCode # Establishes which player is requested
        self.id = self.getPlayerID(self.nameCode)
        self.season = season
        self.statsUrl = f'https://statsapi.web.nhl.com/api/v1/people/{self.id}/stats?stats=statsSingleSeason&season={self.season}'
        self.infoUrl = f'https://statsapi.web.nhl.com/api/v1/people/{self.id}'
        self.stats = self.getStatsDict(self.statsUrl) # Returns a dictionary of the players stats
        self.info = self.getInfoDict(self.infoUrl) # Returns a dictionary of the players info
        self.team = self.getTeamDict(self.info) # Returns a dictionary of the players team
        self.teamId = str(self.team['id'])
        self.teamColour = self.getTeamColour(self.teamId)

    def getPlayerID(self, PlayerName):
        with open('AllTimePlayer.json', 'r+') as f:
            data = json.load(f)
            return(data[PlayerName])
    
    def getTeamColour(self, ID):
        with open('TeamColour.json', 'r+') as f:
            data = json.load(f)
            return data[ID]
    
    def getInfoDict(self, url):
        request = requests.get(url)
        FullName = request.json()['people'][0]
        return FullName

    def getStatsDict(self, url):
        request = requests.get(url)
        stats = request.json()['stats'][0]['splits'][0]['stat']
        return stats
    
    def getTeamDict(self, info):
        team = info['currentTeam']
        return team
    
    def GetPlayerName(self):
        name_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(self.id))
        FullName = name_url.json()['people'][0]['fullName']
        return FullName


class Team: # Designed to be a parent class, which the end user will inherite from
    def __init__(self, teamABBR):
        self.abbr = teamABBR
        self.id = self.getTeamID(self.abbr)
        self.statsUrl = f'https://statsapi.web.nhl.com/api/v1/teams/{self.id}/stats'
        self.infoUrl = f'https://statsapi.web.nhl.com/api/v1/teams/{self.id}'
        self.rosterUrl = f'https://statsapi.web.nhl.com/api/v1/teams/{self.id}?expand=team.roster'
        self.stats = self.getStatsDict(self.statsUrl)
        self.ranks = self.getRanksDict(self.statsUrl)
        self.info = self.getInfoDict(self.infoUrl)
        self.colour = self.getTeamColour(self.id)
        
    def __add__(self, other): # Adding two Team instances together results in the comparison of their Win/Loss record
        return f'{self.abbr}: {self.getWinLoss()} | {other.abbr}: {other.getWinLoss()}'

    def getTeamID(self, abbr):
        try:
            with open('ABBRid.json', 'r+') as f:
                data = json.load(f)
                return data[abbr]
        except:
            raise TeamError("InvalidTeamAbbr")
    
    def GetTeamName(self):
        url = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + str(self.id))
        name = url.json()['teams'][0]['name']
        return name

    def getWinLoss(self):
        win = self.stats['wins']
        loss = self.stats['losses']
        ot = self.stats['ot']
        point = self.stats['pts']
        return '({}/{}/{}/{})'.format(win, loss, ot, point)

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
    
    def getRosterList(self, url): # Returns a list of all players on the team's roster.
        request = requests.get(url)
        roster = request.json()['teams'][0]['roster']['roster']
        return roster

    def getSkaterIds(self): # Returns a list of all skater IDs on the roster. 
        rosterList = self.getRosterList(self.rosterUrl)
        rosterIdList = []
        for person in rosterList:
            if person['position']['code'] != 'G':
                rosterIdList.append(person['person']['id'])
        return rosterIdList

    def getGoalieIds(self): # Returns a list of all goalie IDs on the roster. 
        rosterList = self.getRosterList(self.rosterUrl)
        rosterIdList = []
        for person in rosterList:
            if person['position']['code'] == 'G':
                rosterIdList.append(person['person']['id'])
        return rosterIdList

    def getTeamStatLeaders(self, statRequested= 'points'): # Returns a dictionary containing a stat of all players order from high to low. All stats are integers.
        skaters = self.getSkaterIds() # Time stats (timeOnIce) are returned in seconds. The accepted stat codes can be viewed through the player class.
        statDict = {}
        year = GetCurrentSeason()
        for id in skaters:
            url = f'https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=statsSingleSeason&season={year}'
            try: # Skips any players that are on the roster but never register any ice time.
                allStats = requests.get(url).json()['stats'][0]['splits'][0]['stat']
                try:
                    stat = allStats[statRequested]
                except:
                    raise TeamError('InvalidStatCode')
                if len(str(stat).split(':')) > 1:
                    splitTime = str(stat).split(':')
                    minutes = splitTime[0]
                    seconds = int(minutes) * 60
                    stat = seconds + int(splitTime[1])
                statDict[id] = stat
            except:
                pass
        sortedstatDict = {k: v for k, v in sorted(statDict.items(), key=lambda item: item[1])}
        sortedId = reversed(list(sortedstatDict.keys()))
        sortedstat = reversed(list(sortedstatDict.values()))
        statLeaders = dict(zip(sortedId, sortedstat))
        return statLeaders


class MatchUp: # Returns most of the endpoints for gathering game data. The data is in a raw form, use the Game class for game stats
    def __init__(self, team, date):
        self.scheduleUrl = f'https://statsapi.web.nhl.com/api/v1/schedule?teamId={team}&date={date}'
        self.schedule = self.getScheduleDict(self.scheduleUrl)
        self.id = self.getGameId(self.schedule)
        self.boxscoreUrl = f'https://statsapi.web.nhl.com/api/v1/game/{self.id}/boxscore'
        self.linescoreUrl = f'https://statsapi.web.nhl.com/api/v1/game/{self.id}/linescore'
        self.livefeedUrl = f'https://statsapi.web.nhl.com/api/v1/game/{self.id}/feed/live'
        self.boxscore = self.getBoxscoreDict(self.boxscoreUrl)
        self.linescore = self.getLinescoreDict(self.linescoreUrl)
        self.liveGameInfo = self.getLiveGameInfoDict(self.livefeedUrl)
        self.livefeed = self.getLivefeedDict(self.livefeedUrl)
        self.teams = self.linescore['teams']
        self.home = self.teams['home']['team']
        self.away = self.teams['away']['team']


    def getGameId(self, schedule): # Returns the ID (or as the NHL API refers: PK) of the game of the passed date and team.
        try:          
            pk = schedule['dates'][0]['games'][0]['gamePk']
            return str(pk)
        except: 
            raise DateError(f"No game found")

    def getBoxscoreDict(self, url):
        request = requests.get(url)
        boxscore = request.json()['teams']
        return boxscore
    
    def getLinescoreDict(self, url):
        request  = requests.get(url)
        linescore = request.json()
        return linescore

    def getScheduleDict(self, url):
        request = requests.get(url)
        schedule = request.json()
        return schedule

    # Returns a massive dictionary containing every event of the game. Averages arround 14k lines. It is split in two major sections, hence the two functions.
    def getLiveGameInfoDict(self, url):
        request = requests.get(url)
        livefeed = request.json()['gameData']
        return livefeed
    
    def getLivefeedDict(self, url):
        request = requests.get(url)
        livefeed = request.json()['liveData']
        return livefeed

class Game(MatchUp): # Inherits from the MatchUp class, using the endpoints gathered with that class on order to return refined games stats
    def __init__(self, id, date):
        MatchUp.__init__(self, id, date)
        self.homeStats = self.getHomeStatsDict(self.boxscore)
        self.awayStats = self.getAwayStatsDict(self.boxscore)
        self.homeGoals = self.getStat(self.homeStats, 'goals')
        self.awayGoals = self.getStat(self.awayStats, 'goals')
        self.homeShots = self.getStat(self.homeStats, 'shots')
        self.awayShots = self.getStat(self.awayStats, 'shots')
        self.homeHits = self.getStat(self.homeStats, 'hits')
        self.awayHits = self.getStat(self.awayStats, 'hits')
        self.homeBlocked = self.getStat(self.homeStats, 'blocked')
        self.awayBlocked = self.getStat(self.awayStats, 'blocked')
        self.homePIM = self.getStat(self.homeStats, 'pim')
        self.awayPIM = self.getStat(self.awayStats, 'pim')
        self.homePowerPlayPercentage = self.getStat(self.homeStats, 'powerPlayPercentage')
        self.awayPowerPlayPercentage = self.getStat(self.awayStats, 'powerPlayPercentage')
        self.homePowerPlayGoals = self.getStat(self.homeStats, 'powerPlayGoals')
        self.awayPowerPlayGoals = self.getStat(self.awayStats, 'powerPlayGoals')
        self.homePowerPlayOpportunities = self.getStat(self.homeStats, 'powerPlayOpportunities')
        self.awayPowerPlayOpportunities = self.getStat(self.awayStats, 'powerPlayOpportunities')
        self.homeFaceOffWinPercentage = self.getStat(self.homeStats, 'faceOffWinPercentage')
        self.awayFaceOffWinPercentage = self.getStat(self.awayStats, 'faceOffWinPercentage')
        self.homeTakeaway = self.getStat(self.homeStats, 'takeaways')
        self.awayTakeaway = self.getStat(self.awayStats, 'takeaways')
        self.homeGiveaways = self.getStat(self.homeStats, 'giveaways')
        self.awayGiveaways = self.getStat(self.awayStats, 'giveaways')
        self.goalies = self.getGoalieIds(self.boxscore)
        self.period = self.getCurrentPeriod(self.linescore)
        self.timeRemaining = self.getPeriodTime(self.linescore)
        self.intermission = self.getIntStatus(self.linescore)
        self.intermissionTime = self.intTimeRemaining(self.linescore)
        self.gameStars = self.getGameStars(self.livefeed)
        self.firstStar = self.gameStars[0]
        self.secondStar = self.gameStars[1]
        self.thirdStar = self.gameStars[2]

# Boxscore Functions

    def getHomeStatsDict(self, boxscore): # Returns a dictionary of the primary stats for the home team. Helpful reference for the requestedStat in getStat.
        stats = boxscore['home']['teamStats']['teamSkaterStats']
        return stats

    def getAwayStatsDict(self, boxscore): # Returns a dictionary of the primary stats for the away team. Helpful reference for the requestedStat in getStat.
        stats = boxscore['away']['teamStats']['teamSkaterStats']
        return stats

    def getStat(self, teamStats, requestedStat): # Takes the dictionary return in the getHomeStatsDict and getAwayStatsDict and a stat code and returns the value.
        stat = teamStats[requestedStat]
        return stat

    def getGoalieIds(self, boxscore): # Returns a dictionary with the player IDs of all goalies who dressed for the match, or the goalies who logged ice time when the match is final
        teams = ['home', 'away']
        allGoalies = {}
        for team in teams:
            goalies = boxscore[team]['goalies']
            allGoalies[team] = goalies
        return allGoalies

# Linescore Functions

    def getCurrentPeriod(self, linescore):
        period = linescore['currentPeriodOrdinal']
        return period

    def getGamePeriods(self, linescore):  # Returns a list of all periods that took place during the game, including all overtime periods.
        periods = linescore["periods"]
        return periods

    def getPeriodStartTime(self, period=None): # Interates over the list returned by getGamePeriods in order to return the exact start time in UTC of the requested period.
        periodList = self.getGamePeriods(self.linescore) # Returns all start times by default, can be provided an index value to return specific period start times.
        if period == None:
            timesDict = {}
            for i, per in enumerate(periodList):
                num = periodList[i]['ordinalNum']
                startTime = periodList[i]['startTime']
                timesDict[num] = startTime
            return timesDict

        elif period < 0:
            raise PeriodError("NegValue")
        elif period > len(periodList) - 1:
            raise PeriodError("ValueOutOfRange")
        else:
            startTime = periodList[period]['startTime']
            return startTime

    def getPeriodEndTime(self, period=None): # Interates over the list returned by getGamePeriods in order to return the exact end time in UTC of the requested period.
        periodList = self.getGamePeriods(self.linescore) # Returns all end times by default, can be provided an index value to return specific period end times.
        if period == None:
            timesDict = {}
            for i, per in enumerate(periodList):
                num = periodList[i]['ordinalNum']
                try:
                    endTime = periodList[i]['endTime']
                except:
                    endTime = 'TBD'
                timesDict[num] = endTime
            return timesDict

        elif period < 0:
            raise PeriodError("NegValue")
        elif period > len(periodList) - 1:
            raise PeriodError("ValueOutOfRange")
        else:
            endTime = periodList[period]['endTime']
            return endTime

    def getPeriodTime(self, linescore):
        timeRemaining = linescore['currentPeriodTimeRemaining']
        return timeRemaining
    
    def getIntStatus(self, linescore):
        intermission  = linescore['intermissionInfo']['inIntermission']
        return intermission
    
    def intTimeRemaining(self, linescore):
        if self.getIntStatus(self.linescore):
            time = linescore['intermissionInfo']['intermissionTimeRemaining']
            timeRemaining = time / 60
            return timeRemaining
        else:
            return None

# Schedule Functions

    def getGameStatusCode(self, schedule):
        statusCode = schedule['dates'][0]['games'][0]['status']['statusCode']
        return statusCode
    
    def getGameStatus(self, schedule):
        status = schedule['dates'][0]['games'][0]['status']['detailedState']
        return status

    def getHomeTeamRecord(self, schedule): # Returns a list holding the season record of the home team of the matchup
        record = schedule['dates'][0]['games'][0]['teams']['home']['leagueRecord']
        wins = record['wins']
        losses = record['losses']
        try:
            ot = record['ot']
        except:
            ot = 'N/A'
        recordls = [wins, losses, ot]
        return recordls

    def getAwayTeamRecord(self, schedule): # Returns a list holding the season record of the away team of the matchup
        record = schedule['dates'][0]['games'][0]['teams']['away']['leagueRecord']
        wins = record['wins']
        losses = record['losses']
        try:
            ot = record['ot']
        except:
            ot = 'N/A'
        recordls = [wins, losses, ot]
        return recordls

#Livefeed Functions

    def getGameStars(self, livefeed): # Returns a list of the stars of the game. If the stars are undecided, or unavailible, an empty list is returned.
        stars = []
        try:
            decision = livefeed['decisions']
            stars.extend((decision['firstStar'], decision['secondStar'], decision['thirdStar']))
            return stars
        except:
            return stars