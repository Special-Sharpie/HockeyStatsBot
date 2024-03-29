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
    "ET" : "Canada/Eastern",
    "CET" : "CET",
    "EET" : "EET",
    "WET": "WET"
}

def next(teamID, code):
    # getting the dates to check for previous games
    tday = datetime.datetime.now(pytz.timezone('Canada/Mountain')).date()
    i = 1
    while i <= 10:
        next = tday + timedelta(days=i)

        # urls used to check the last 10 days for hockey games
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
            FGaway = data['away']['team']['name']
            return ('The next game will see the ' + FGhome + ' host the ' + FGaway + ' on ' + str(game_dt) + ' {}.'.format(code))
        except:
            if i == 10:
                return ("No up coming games!")
            else:
                i += 1

