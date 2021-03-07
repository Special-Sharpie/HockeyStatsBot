import json
import pprint as p
import requests as r
import botLogic as bot

def skaterStats(player):
    url = r.get('https://statsapi.web.nhl.com/api/v1/people/' + player + '/stats?stats=yearByYear')
    playername = bot.GetPlayerName(player)
    yearByYear = url.json()['stats'][0]['splits']
    TGP = 0
    TG = 0
    TA = 0
    TP = 0
    TPM = 0
    TPIM = 0
    TPPG = 0
    TPPP = 0
    TSHG = 0
    TSHP = 0
    TGWG = 0
    TOTG = 0
    TS = 0
    ls = []

    with open('career.txt', 'a') as f:
        x = 'Season: Team | GP | G | A | P | +/- | PIM | PPG | SHG '
        i = 0
        while i < len(yearByYear):
            league = yearByYear[i]['league']['name']
            if league == "National Hockey League":
                yearStats = yearByYear[i]
                seasonAPI = yearStats['season']
                season = seasonAPI[:4] + '-' + seasonAPI[4:]
                G = yearStats['stat']['goals']
                Team = yearStats['team']['id']
                GP = yearStats['stat']['games']
                A = yearStats['stat']['assists']
                P = yearStats['stat']['points']
                PM = yearStats['stat']['plusMinus']
                PIM = yearStats['stat']['pim']
                PPG = yearStats['stat']['powerPlayGoals']
                PPP = yearStats['stat']['powerPlayPoints']
                SHG = yearStats['stat']['shortHandedGoals']
                SHP = yearStats['stat']['shortHandedPoints']
                GWG = yearStats['stat']['gameWinningGoals']
                OTG = yearStats['stat']['overTimeGoals']
                S = yearStats['stat']['shots']
                TGP += GP
                TG += G
                TA += A
                TP += P
                TPM += PM
                TPIM += PIM
                TPPG += PPG
                TPPP += PPP
                TSHG += SHG
                TSHP += SHP
                TGWG += GWG
                TOTG += OTG
                TS += S

                abbr = bot.getOtherAbbr(str(Team))

                f.write('{}: {} | {} | {} | {} | {} | {} | {} | {} | {}   '.format(season, abbr, GP, G, A, P, PM, PIM, PPG, SHG) + '\n')
                i += 1

            else:
                i += 1

        totals =('Total:  GP:{} | G:{} | A:{} | P:{} | +/-:{} | PIM:{} | PPG:{} | SHG:{}  '.format(TGP, TG, TA, TP, TPM, TPIM, TPPG, TSHG))

    with open('career.txt', 'r+') as f:
        Career = f.read()
        ls.extend((x, Career, totals))
        f.truncate(0)
    return ls

#print(len(CareerStats('8465009')[0]))

