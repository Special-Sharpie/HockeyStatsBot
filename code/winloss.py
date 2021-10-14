import random
import json
import requests
import pprint
import botLogic
def winloss(FranID1, FranID2):
    ls = []
    teamA = botLogic.readJSON('franId.json', FranID1)
    teamB = botLogic.readJSON('franId.json', FranID2)
    url = requests.get('https://records.nhl.com/site/api/all-time-record-vs-franchise?cayenneExp=teamFranchiseId=' + str(teamA))
    indexPos = url.json()['data']
    record = url.json()['data'][botLogic.findOppIndex(indexPos, 'opponentFranchiseId', int(teamB))]
    homeWIN = record['homeWins']
    homeLOSS = record['homeLosses']
    homeOT = record['homeOtLosses']
    homeT = record['homeTies']
    roadWIN = record['roadWins']
    roadLOSS = record['roadLosses']
    roadOT = record['roadOtLosses']
    roadT = record['roadTies']
    totalWIN = record['totalWins']
    totalLOSS = record['totalLosses']
    totalOT = record['totalOtLosses']
    totalT = record['totalTies']
    Tname = record['franchiseName']
    OPPname = record['opponentFranchiseName']
    ls.extend((Tname, OPPname, homeWIN, homeLOSS, homeOT, homeT, roadWIN, roadLOSS, roadOT, roadT, totalWIN, totalLOSS, totalOT, totalT))
    return ls
