import requests as r

def draft(requestedYear, requestedTeam):
    url = r.get('https://statsapi.web.nhl.com/api/v1/draft/{}'.format(requestedYear))
    rounds = {}
    draftData = url.json()['drafts'][0]['rounds']
    m = 0
    while m < len(draftData):
        roundNumber = draftData[m]['round']
        roundNumber = ('Round: {}'.format(roundNumber))
        roundData = draftData[m]['picks']
        drafts = []
        i = 0
        while i < len(roundData):
            pickOverall = roundData[i]['pickOverall']
            pickInRound = roundData[i]['pickInRound']
            team = roundData[i]['team']['id']
            name = roundData[i]['prospect']['fullName']
            if team == int(requestedTeam):
                drafts.append("{}, Rank: {}, Overall: {}".format(name, pickInRound, pickOverall))
                rounds[roundNumber] = drafts
            i += 1
        m += 1
    return rounds
