import json
import requests
import pprint
import datetime
import pytz
import botLogic

tz={
    "PT" : "Canada/Pacific",
    "MT" : "Canada/Mountain",
    "CT" : "Canada/Central",
    "ET" : "Canada/Eastern"
}

def daySumDate(RequestedDate):
    ls = []
    url = requests.get('http://statsapi.web.nhl.com/api/v1/schedule?date={}'.format(RequestedDate))
    date = url.json()['dates'][0]['date']
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')

    game_dt = datetime.datetime.strftime(dt, '%A, %B %d, %Y')

    numOfGames = url.json()['dates'][0]['games']
    ls.extend((len(numOfGames), game_dt))
    return ls

def daySum(i, TZ, RequestedDate):
    url = requests.get('http://statsapi.web.nhl.com/api/v1/schedule?date={}'.format(RequestedDate))
    numOfGames = url.json()['dates'][0]['games']
    ls = []
    code = numOfGames[i]['status']['statusCode']
    if int(code) < 3:
        data = numOfGames[i]['teams']
        awayName = data['away']['team']['name']
        homeName = data['home']['team']['name']
        awayID = data['away']['team']['id']
        homeID = data['home']['team']['id']

        aAbbr = botLogic.getOtherAbbr(str(awayID))
        hAbbr = botLogic.getOtherAbbr(str(homeID))

        time = numOfGames[i]['gameDate']
        dt = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        dt_utc = pytz.timezone('UTC')
        cad_mtn = pytz.timezone('Canada/Mountain')
        dt = dt_utc.localize(dt)
        dt_mtn = dt.astimezone(pytz.timezone(tz[TZ]))
        game_dt = datetime.datetime.strftime(dt_mtn, '%I:%M%p {}'.format(TZ))

        ls.extend((awayName, homeName, aAbbr, hAbbr, game_dt))
        return ls

    else:
        data = numOfGames[i]['teams']
        awayName = data['away']['team']['name']
        homeName = data['home']['team']['name']
        awayID = data['away']['team']['id']
        homeID = data['home']['team']['id']

        aAbbr = botLogic.getOtherAbbr(str(awayID))
        hAbbr = botLogic.getOtherAbbr(str(homeID))

        awayScore = data['away']['score']
        homeScore = data['home']['score']
        state = numOfGames[i]['status']['detailedState']

        ls.extend((awayName, homeName, aAbbr, hAbbr, awayScore, homeScore, state))
        return ls

