import hockeyPy

def teamInfo(abbr):
    Team = hockeyPy.Team(abbr)
    infoLs = []
    info = Team.info
    colour = Team.colour

    name = info['teamName']
    city = info['locationName']
    div = info['division']['name']
    conf = info['conference']['name']
    venue = info['venue']['name']
    firstYear = info['firstYearOfPlay']
    teamUrl = info['officialSiteUrl']
    collectedInfo = 'Team Name: {}\nCity: {}\nVenue: {}\nFirst Year: {}\nDivision: {}\nConference: {}\nAbbreviation: {}\nWebsite: {}'.format(name, city, venue, firstYear, div, conf, abbr, teamUrl)
    infoLs.extend((name, collectedInfo, colour))
    return infoLs
