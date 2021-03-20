import requests
import json
import pprint
import datetime
from datetime import timedelta
import pytz

tz={
    "PT" : "Canada/Pacific",
    "MT" : "Canada/Mountain",
    "CT" : "Canada/Central",
    "ET" : "Canada/Eastern"
}

def next(teamID, code):
    # getting the dates to check for previous games
    tday = datetime.datetime.now(pytz.timezone('Canada/Mountain')).date()
    i = 1
    while i <= 10:
        d = datetime.date(2020, 1, 17)
        next = tday + timedelta(days=i)

        # urls for used to check the last 10 days for hockey games
        api_url = requests.get(
        'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(teamID) + '&startDate=' + str(next) + '&endDate=' + str(next))
        try:

            FGdate = api_url.json()['dates'][0]['games'][0]['gameDate']
            dt = datetime.datetime.strptime(FGdate, '%Y-%m-%dT%H:%M:%SZ')
            dt_utc = pytz.timezone('UTC')
            dt = dt_utc.localize(dt)
            dt_mtn = dt.astimezone(pytz.timezone(tz[code]))

            game_dt = datetime.datetime.strftime(dt_mtn, '%A, %B %d, %Y at %I:%M%p')

            data = api_url.json()['dates'][0]['games'][0]['teams']
            FGhome = data['home']['team']['name']
            FGhomeScore = data['home']['score']
            print(FGhomeScore)
            FGaway = data['away']['team']['name']
            FGawayScore = data['away']['score']
            return ('The next game will see the ' + FGhome + ' host the ' + FGaway + ' on ' + str(game_dt) + ' {}.'.format(code))
            #print('game', i)
            i += 1
            break
        except:
            if i == 10:
                return ("No up coming games!")
                break
            else:
                i += 1

