import datetime
from datetime import timedelta
import requests as r
import json
import pprint as p
import pytz

tz={
    "PT" : "Canada/Pacific",
    "MT" : "Canada/Mountain",
    "CT" : "Canada/Central",
    "ET" : "Canada/Eastern"
}

def sched(ID, code):
    tday = datetime.date.today()
    length = 8
    testedLS = {}
    i = 1

    def check(i):
        day = tday + timedelta(days = i)
        url = r.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId={}&startDate={}&endDate={}'.format(ID, day, day))
        data = url.json()
        try:
            dateData = []
            gameDate = data['dates'][0]['games'][0]['gameDate']
            homeTeam = data['dates'][0]['games'][0]['teams']['home']['team']['name']
            awayTeam = data['dates'][0]['games'][0]['teams']['away']['team']['name']

            dt = datetime.datetime.strptime(gameDate, '%Y-%m-%dT%H:%M:%SZ')
            dt_utc = pytz.timezone('UTC')
            dt = dt_utc.localize(dt)
            dt_mtn = dt.astimezone(pytz.timezone(tz[code]))
            game_time = datetime.datetime.strftime(dt_mtn, '%I:%M%p {}'.format(code))
            game_dt = datetime.datetime.strftime(dt_mtn, '%A, %B %d, %Y')

            dateData.extend((game_time, homeTeam, awayTeam))
            testedLS[game_dt] = dateData
        except:
            dt = datetime.datetime.strptime(str(day), '%Y-%m-%d')
            dt = datetime.datetime.strftime(dt, '%A, %B %d, %Y')
            testedLS[str(dt)] = 'No Game!'
        i += 1
        if i != length:
            check(i)
    check(i)
    return testedLS


'''
for i in x:
    date = x[i]
    if type(date) == list:
        print(i, ':', date[1], date[2], date[0])
    else:
        print(i, ':', date)
#p.pprint(testedLS)
'''
