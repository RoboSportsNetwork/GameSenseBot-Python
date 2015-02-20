import TbaApi as api
import TbaApiSettings
from urllib2 import Request, urlopen, HTTPError
import json


def getTeam(teamKey):
    url = TbaApiSettings.tbaBaseUrl + '/team/' + str(teamKey)
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    team = api.TbaTeam()
    return team.deserialize(json_obj)


def getEvent(eventKey):
    url = TbaApiSettings.tbaBaseUrl + '/event/' + str(eventKey)
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    event = api.TbaEvent()
    return event.deserialize(json_obj)


def getTeamEvents(teamKey, year):
    url = TbaApiSettings.tbaBaseUrl + '/team/' + \
        teamKey + '/' + year + '/events'
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    teamEvents = []
    for item in json_obj:
        event = api.TbaEvent()
        event.deserialize(item)
        teamEvents.append(event)

    return teamEvents


def getTeamEventMatches(teamKey, eventKey):
    url = TbaApiSettings.tbaBaseUrl + "/team/" + \
        teamKey + "/event/" + eventKey + "/matches"
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    teamEventMatches = []
    for item in json_obj:
        match = api.TbaMatch()
        match.deserialize(item)
        teamEventMatches.append(match)

    return teamEventMatches


def getTeamRecordInMatches(teamKey, matches):
    record = api.TbaTeamRecord()

    for match in matches:
        if (match.alliances.blue.score > match.alliances.red.score):
            if(teamKey in match.alliances.blue.teams):
                record.wins += 1
            else:
                record.losses += 1
        elif (match.alliances.red.score > match.alliances.blue.score):
            if(teamKey in match.alliances.red.teams):
                record.wins += 1
            else:
                record.losses += 1
        else:
            record.ties += 1

    return record


def getAllTeamMatches(teamKey, year):
    matches = []
    events = getTeamEvents(teamKey, year)

    for evt in events:
        matches.extend(
            getTeamEventMatches(teamKey, evt.key))

    return matches


def getMatch(eventCode, matchCode):
    url = TbaApiSettings.tbaBaseUrl + '/match/' + eventCode + '_' + matchCode
    api_response_string = send_and_get_response(url)
    if not api_response_string:
        match = None
    else:
        json_obj = json.loads(api_response_string)
        match = api.TbaMatch()
        match.deserialize(json_obj)

    return match

def getEventAwards(eventCode):
    url = TbaApiSettings.tbaBaseUrl + '/event/' + eventCode + '/awards'
    api_response_string = send_and_get_response(url)
    
    if not api_response_string:
        awards = None
    else:
        json_obj = json.loads(api_response_string)
        awards = []
        for item in json_obj:
            award = api.TbaAward()
            award.deserialize(item)
            awards.append(award)

    return awards


def getTeamEventAwards(teamKey, eventCode):
    url = TbaApiSettings.tbaBaseUrl + '/team/' + teamKey + '/event/' + eventCode + '/awards'
    api_response_string = send_and_get_response(url)

    if not api_response_string:
        awards = None
    else:
        json_obj = json.loads(api_response_string)
        awards = []
        for item in json_obj:
            award = api.TbaAward()
            award.deserialize(item)
            awards.append(award)
    return awards


def getTeamYearAwards(teamKey, year):
    events = getTeamEvents(teamKey, year)
    awards = []
    for evt in events:
        awards.extend(getTeamEventAwards(teamKey, evt.key))

    return awards


def send_and_get_response(uri):
    request = Request(uri)
    Request.add_header(request, "X-TBA-App-Id", "gamesense:gamesensebot:v02")
    try:
        response_body = urlopen(request).read()
        return response_body
    except HTTPError:
        return None
