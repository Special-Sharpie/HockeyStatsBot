import json
import requests
import botLogic
import datetime
import pytz

tz={
    "PT" : "Canada/Pacific",
    "MT" : "Canada/Mountain",
    "CT" : "Canada/Central",
    "ET" : "Canada/Eastern"
}

def gday(ID, TZ):
    # url for currnet day hockey game
    lst = []
    preList = []
    postList = []
    tday = datetime.datetime.now(pytz.timezone('Canada/Mountain')).date()
    url = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(ID) + '&startDate=' + str(tday) +'&endDate=' + str(tday))
    url2 = requests.get('https://statsapi.web.nhl.com/api/v1/game/'+botLogic.getGamePK(ID)+'/linescore')


    code = url.json()['dates'][0]['games'][0]['status']['statusCode']
    date = url.json()['dates'][0]['games'][0]['gameDate']
    data = url.json()['dates'][0]['games'][0]['teams']
    shots = url2.json()['teams']
    awayTeam = data['away']['team']['name']
    awayID = data['away']['team']['id']
    awayGoals = data['away']['score']
    awayShots = shots['away']['shotsOnGoal']
    homeTeam = data['home']['team']['name']
    homeID = data['home']['team']['id']
    homeGoals = data['home']['score']
    homeShots = shots['home']['shotsOnGoal']

    aId = botLogic.getOtherAbbr(str(awayID))
    hId = botLogic.getOtherAbbr(str(homeID))

    lst.extend((code, awayTeam, homeTeam, aId, hId, str(awayGoals), str(homeGoals), str(awayShots), str(homeShots), str(tday)))
    dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    dt_utc = pytz.timezone('UTC')
    dt = dt_utc.localize(dt)
    dt_mtn = dt.astimezone(pytz.timezone(tz[TZ]))
    game_dt = datetime.datetime.strftime(dt_mtn, '%I:%M%p {}'.format(TZ))
    preList.extend((code, awayTeam, homeTeam, game_dt))
    postList.extend((code, awayTeam, homeTeam, aId, hId, str(awayGoals), str(homeGoals), str(awayShots), str(homeShots), str(tday)))
    if int(code) < 3:
        return preList # Pre
    elif int(code) > 4:
        final = postList
        return final #final
    else:
        return lst #Current
