import json
import requests
import botLogic

def stats(playerID, playoff, season):
    ls = []
    isGoalie = botLogic.getPlayerType(playerID)
    if playoff == 'R':
        stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeason&season=' + str(season))
        #stat = stats_url.json()['stats'][0]['splits'][0]['stat']
        if not isGoalie:
            playerTOI = stats_url.json()['stats'][0]['splits'][0]['stat']['timeOnIce']
            playerAssists = stats_url.json()['stats'][0]['splits'][0]['stat']['assists']
            playerGoals = stats_url.json()['stats'][0]['splits'][0]['stat']['goals']
            playerPIM = stats_url.json()['stats'][0]['splits'][0]['stat']['pim']
            playerShots = stats_url.json()['stats'][0]['splits'][0]['stat']['shots']
            playerGames = stats_url.json()['stats'][0]['splits'][0]['stat']['games']
            playerHits = stats_url.json()['stats'][0]['splits'][0]['stat']['hits']
            playerPPG = stats_url.json()['stats'][0]['splits'][0]['stat']['powerPlayGoals']
            playerPPP = stats_url.json()['stats'][0]['splits'][0]['stat']['powerPlayPoints']
            playerGWG = stats_url.json()['stats'][0]['splits'][0]['stat']['gameWinningGoals']
            playerBlocked = stats_url.json()['stats'][0]['splits'][0]['stat']['blocked']
            playerPM = stats_url.json()['stats'][0]['splits'][0]['stat']['plusMinus']
            playerPoints = stats_url.json()['stats'][0]['splits'][0]['stat']['points']
            playerOTgoals = stats_url.json()['stats'][0]['splits'][0]['stat']['overTimeGoals']
            playerShortHanded = stats_url.json()['stats'][0]['splits'][0]['stat']['shortHandedGoals']
            name = botLogic.GetPlayerName(playerID)
            x = ('Goals: ' + str(playerGoals) + '\n' + 'Assits: ' + str(playerAssists) + '\n' + 'Points: ' + str(playerPoints) + '\n' + 'Shots: ' + str(playerShots) + '\n' + 'Overtime Goals: ' + str(playerOTgoals)
                              + '\n' + 'Short Handed Goals: ' + str(playerShortHanded) + '\n' + 'Plus/Minus: ' + str(playerPM) + '\n' + 'Time On Ice: ' + str(playerTOI) + '\n' + 'Games Played: ' + str(playerGames) + '\n' + 'Power Play Goals: ' + str(playerPPG)
                              + '\n' + 'Power Play Points: ' + str(playerPPP) + '\n' + 'Game Winning Goals: ' + str(playerGWG) + '\n' + 'Penalties In Minutes: ' + str(playerPIM) + '\n' +
                              'Hits: ' + str(playerHits) + '\n' + 'Blocked Shots: ' + str(playerBlocked))
            ls.append(name)
            ls.append(x)
            return ls
        else:
            goalieTOI = stats_url.json()['stats'][0]['splits'][0]['stat']['timeOnIce']#done
            goalieOT = stats_url.json()['stats'][0]['splits'][0]['stat']['ot']
            goalieSO = stats_url.json()['stats'][0]['splits'][0]['stat']['shutouts']
            goalieWins = stats_url.json()['stats'][0]['splits'][0]['stat']['wins']
            goalieLosses = stats_url.json()['stats'][0]['splits'][0]['stat']['losses']
            goalieSaves = stats_url.json()['stats'][0]['splits'][0]['stat']['saves']
            goalieSP = stats_url.json()['stats'][0]['splits'][0]['stat']['savePercentage']
            goalieGAA = stats_url.json()['stats'][0]['splits'][0]['stat']['goalAgainstAverage']
            goalieGames = stats_url.json()['stats'][0]['splits'][0]['stat']['games']
            goalieSA = stats_url.json()['stats'][0]['splits'][0]['stat']['shotsAgainst']
            goalieGA = stats_url.json()['stats'][0]['splits'][0]['stat']['goalsAgainst']
            name = botLogic.GetPlayerName(playerID)
            x = ('Wins: ' + str(goalieWins) + '\n' + 'Losses: ' + str(goalieLosses) + '\n' + 'Over Time Losses: ' + str(goalieOT) + '\n' + 'Shutouts: ' + str(goalieSO) + '\n' +
                                   'Time On Ice: ' + str(goalieTOI) + '\n' + 'Games: ' + str(goalieGames) + '\n' + 'Save Percentage: ' + str(goalieSP) + '\n' + 'Goals Against Average: ' +
                                   str(goalieGAA) + '\n' + 'Saves: ' + str(goalieSaves) + '\n' + 'Shots Against: ' + str(goalieSA) + '\n' + 'Goals Against: ' + str(goalieGA) + '\n')
            ls.append(name)
            ls.append(x)
            return ls
    elif playoff == 'P':
        stats_url = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(playerID) + '/stats?stats=statsSingleSeasonPlayoffs&season=' + str(season))
        if not isGoalie:
            playerTOI = stats_url.json()['stats'][0]['splits'][0]['stat']['timeOnIce']
            playerAssists = stats_url.json()['stats'][0]['splits'][0]['stat']['assists']
            playerGoals = stats_url.json()['stats'][0]['splits'][0]['stat']['goals']
            playerPIM = stats_url.json()['stats'][0]['splits'][0]['stat']['pim']
            playerShots = stats_url.json()['stats'][0]['splits'][0]['stat']['shots']
            playerGames = stats_url.json()['stats'][0]['splits'][0]['stat']['games']
            playerHits = stats_url.json()['stats'][0]['splits'][0]['stat']['hits']
            playerPPG = stats_url.json()['stats'][0]['splits'][0]['stat']['powerPlayGoals']
            playerPPP = stats_url.json()['stats'][0]['splits'][0]['stat']['powerPlayPoints']
            playerGWG = stats_url.json()['stats'][0]['splits'][0]['stat']['gameWinningGoals']
            playerBlocked = stats_url.json()['stats'][0]['splits'][0]['stat']['blocked']
            playerPM = stats_url.json()['stats'][0]['splits'][0]['stat']['plusMinus']
            playerPoints = stats_url.json()['stats'][0]['splits'][0]['stat']['points']
            playerOTgoals = stats_url.json()['stats'][0]['splits'][0]['stat']['overTimeGoals']
            playerShortHanded = stats_url.json()['stats'][0]['splits'][0]['stat']['shortHandedGoals']
            name = botLogic.GetPlayerName(playerID)
            x = ('Goals: ' + str(playerGoals) + '\n' + 'Assits: ' + str(playerAssists) + '\n' + 'Points: ' + str(playerPoints) + '\n' + 'Shots: ' + str(playerShots) + '\n' + 'Overtime Goals: ' + str(playerOTgoals)
                              + '\n' + 'Short Handed Goals: ' + str(playerShortHanded) + '\n' + 'Plus/Minus: ' + str(playerPM) + '\n' + 'Time On Ice: ' + str(playerTOI) + '\n' + 'Games Played: ' + str(playerGames) + '\n' + 'Power Play Goals: ' + str(playerPPG)
                              + '\n' + 'Power Play Points: ' + str(playerPPP) + '\n' + 'Game Winning Goals: ' + str(playerGWG) + '\n' + 'Penalties In Minutes: ' + str(playerPIM) + '\n' +
                              'Hits: ' + str(playerHits) + '\n' + 'Blocked Shots: ' + str(playerBlocked))
            ls.append(name)
            ls.append(x)
            return ls
        else:
            goalieTOI = stats_url.json()['stats'][0]['splits'][0]['stat']['timeOnIce']#done
            goalieOT = stats_url.json()['stats'][0]['splits'][0]['stat']['ot']
            goalieSO = stats_url.json()['stats'][0]['splits'][0]['stat']['shutouts']
            goalieWins = stats_url.json()['stats'][0]['splits'][0]['stat']['wins']
            goalieLosses = stats_url.json()['stats'][0]['splits'][0]['stat']['losses']
            goalieSaves = stats_url.json()['stats'][0]['splits'][0]['stat']['saves']
            goalieSP = stats_url.json()['stats'][0]['splits'][0]['stat']['savePercentage']
            goalieGAA = stats_url.json()['stats'][0]['splits'][0]['stat']['goalAgainstAverage']
            goalieGames = stats_url.json()['stats'][0]['splits'][0]['stat']['games']
            goalieSA = stats_url.json()['stats'][0]['splits'][0]['stat']['shotsAgainst']
            goalieGA = stats_url.json()['stats'][0]['splits'][0]['stat']['goalsAgainst']
            name = botLogic.GetPlayerName(playerID)
            x = ('Wins: ' + str(goalieWins) + '\n' + 'Losses: ' + str(goalieLosses) + '\n' + 'Over Time Losses: ' + str(goalieOT) + '\n' + 'Shutouts: ' + str(goalieSO) + '\n' +
                                   'Time On Ice: ' + str(goalieTOI) + '\n' + 'Games: ' + str(goalieGames) + '\n' + 'Save Percentage: ' + str(goalieSP) + '\n' + 'Goals Against Average: ' +
                                   str(goalieGAA) + '\n' + 'Saves: ' + str(goalieSaves) + '\n' + 'Shots Against: ' + str(goalieSA) + '\n' + 'Goals Against: ' + str(goalieGA) + '\n')
            ls.append(name)
            ls.append(x)
            return ls