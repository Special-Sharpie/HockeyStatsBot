import json
import botLogic
import hockeyPy

def teamLeaders(teamAbbr, count, stat):
    team = hockeyPy.Team(teamAbbr)
    names = []
    roster = team.getTeamStatLeaders(stat)
    if count > len(roster):
        count = len(roster)
    players = list(roster.keys())[:count]
    amount = list(roster.values())[:count]
    for player in players:
        name = botLogic.GetPlayerName(player)
        names.append(name)  

    with open('statLeader.txt', 'r+') as f:
        i = 0
        while i < len(names):
            f.write(f'{i+1}. {names[i]}: {amount[i]}\n')
            i += 1
    with open('statLeader.txt', 'r+') as f:
        leaders = f.read()
        f.truncate(0)
        return leaders
