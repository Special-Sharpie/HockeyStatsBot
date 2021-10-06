import pprint as p
import requests as r
import botLogic as bot



def skaterStats(player):
    url = r.get('https://statsapi.web.nhl.com/api/v1/people/' + str(player) + '/stats?stats=yearByYear')
    playername = bot.GetPlayerName(player)
    yearByYear = url.json()['stats'][0]['splits']
    ls = []
    seasons = []
    if bot.getPlayerType(player):
        TGP, TSO, TT, TOT, TW, TL, TSP, TGAA, TS= 0, 0, 0, 0, 0, 0, 0, 0, 0
        i = 0
        while i < len(yearByYear):
            league = yearByYear[i]['league']['name']
            if league == "National Hockey League":
                yearStats = yearByYear[i]
                season = yearByYear[i]['season']
                seasons.append(season[:4] + '-' + season[4:])
                statsDictionary = yearStats['stat']
                GP = statsDictionary.get('games', 0)
                SO = statsDictionary.get('shutouts', 0)
                T = statsDictionary.get('ties', 0)
                OT = statsDictionary.get('ot', 0)
                W = statsDictionary.get('wins', 0)
                L = statsDictionary.get('losses', 0)
                SP = statsDictionary.get('savePercentage', 0)
                GAA = statsDictionary.get('goalAgainstAverage', 0)
                # Adds all the year's stats to the totals
                TGP += GP
                TSO += SO
                TT += T
                TOT += OT
                TW += W
                TL += L
                TSP += SP
                TGAA += GAA
                TS += 1
                i += 1
            else:
                i += 1
        TSP /= TS
        TGAA /= TS
        if TSP != 0:
            TSP = f"{TSP:.2f}"
        totals =f"Games Played: {TGP}\nWins: {TW}\nLosses: {TL}\nShutouts: {TSO}\nOver Time Losses: {TOT if TOT != 0 else 'N/A'}\nTies: {TT if TT != 0 else 'N/A'}\nGoals Againts Average: {TGAA:.3f}\nSave Percentage: {'N/A' if TSP == 0 else TSP + '%'}"
    else:
        TGP, TG, TA, TP, TPM, TPIM, TPPG, TSHG = 0, 0, 0, 0, 0, 0, 0, 0
        i = 0
        while i < len(yearByYear):
            league = yearByYear[i]['league']['name']
            if league == "National Hockey League":
                yearStats = yearByYear[i]
                season = yearByYear[i]['season']
                seasons.append(season[:4] + '-' + season[4:])
                statsDictionary = yearStats['stat']
                G = statsDictionary.get('goals', 0)
                GP = statsDictionary.get('games', 0)
                A = statsDictionary.get('assists', 0)
                P = statsDictionary.get('points', 0)
                PM = statsDictionary.get('plusMinus', 0)
                PIM = statsDictionary.get('pim', 0)
                PPG = statsDictionary.get('powerPlayGoals', 0)
                SHG = statsDictionary.get('shortHandedGoals', 0)
                # Adds all the year's stats to the totals
                TGP += GP
                TG += G
                TA += A
                TP += P
                TPM += PM
                TPIM += PIM
                TPPG += PPG
                TSHG += SHG
                i += 1    
            else:
                i += 1
        totals =f"Games Played: {TGP}\nGoals: {TG}\nAssists: {TA}\nPoints: {TP}\nPlus/Minus: {TPM if TPM != 0 else 'N/A'}\nPenalty Infraction Minutes: {TPIM}\nPower Play Goals: {TPPG}\nShort Handed Goals: {TSHG}"
    ls.extend((seasons[0], seasons[-1], playername, totals))
    return ls
