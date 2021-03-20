import requests
import json
import pprint
import datetime
from datetime import timedelta
import pytz
import botLogic

def last(teamID):
    # getting the dates to check for previous games
    ls = []
    tday = datetime.datetime.now(pytz.timezone('Canada/Mountain')).date()
    i = 1
    while i <= 10:
        last = tday - timedelta(days=i)

        # urls for used to check the last 10 days for hockey games
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(teamID) + '&startDate=' + str(last) + '&endDate=' + str(last)
        api_url = requests.get(url)

        try:
            data = api_url.json()['dates'][0]['games'][0]['teams']
            homeName = data['home']['team']['name']
            homeScore = data['home']['score']
            awayName = data['away']['team']['name']
            awayScore = data['away']['score']
            awayID = data['away']['team']['id']
            homeID = data['home']['team']['id']

            date = api_url.json()['dates'][0]['games'][0]['gameDate']
            dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

            dt_utc = pytz.timezone('UTC')

            cad_mtn = pytz.timezone('Canada/Mountain')
            dt = dt_utc.localize(dt)
            dt_mtn = dt.astimezone(pytz.timezone('Canada/Mountain'))

            game_dt = datetime.datetime.strftime(dt_mtn, '%A, %B %d, %Y')

            aAbbr = botLogic.getOtherAbbr(str(awayID))
            hAbbr = botLogic.getOtherAbbr(str(homeID))
            ls.extend((awayName, homeName, str(awayScore), str(homeScore), aAbbr, hAbbr, game_dt, str(last)))
            return ls
            break

        except:
            if i == 10:
                x = "No past games played recently!"
                ls.append(x)
                return ls
                break
            else:
                i += 1

