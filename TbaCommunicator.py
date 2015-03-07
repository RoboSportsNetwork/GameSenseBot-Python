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


def getTeamScoreAvgInMatches(teamKey, matches):
    average = api.TbaTeamScoreAvg()
    playoffMatches = 0
    playoffTotal = 0.0
    qualMatches = 0
    qualTotal = 0.0
    for match in matches:
        if match.alliances.blue.score > 0 and match.alliances.red.score > 0:
            if(teamKey in match.alliances.blue.teams):
                if not match.comp_level == 'qm':
                    playoffMatches += 1
                    playoffTotal += match.alliances.blue.score
                else:
                    qualMatches += 1
                    qualTotal += match.alliances.blue.score
            if(teamKey in match.alliances.red.teams):
                if not match.comp_level == 'qm':
                    playoffMatches += 1
                    playoffTotal += match.alliances.red.score
                else:
                    qualMatches += 1
                    qualTotal += match.alliances.red.score
    if playoffMatches != 0:
        average.playoffAvg = playoffTotal/playoffMatches
    else:
        average.PlayoffAvg = 0
    if qualMatches != 0:
        average.qualAvg = qualTotal/qualMatches
    else:
        average.qualAvg = 0
    return average


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


def get2015EventRankings(eventKey):
    url = TbaApiSettings.tbaBaseUrl + '/event/' + eventKey + '/rankings'
    api_response_string = send_and_get_response(url)

    if not api_response_string:
        rankings = None
    else:
        json_obj = json.loads(api_response_string)
        rankings = []
        for item in json_obj[1:]:  #skip the descriptor
            ranking = api.Tba2015Ranking()
            ranking.deserialize(item)
            rankings.append(ranking)
    return rankings


def get2015TeamRankingAtEvent(teamKey, eventKey):
    rankings = get2015EventRankings(eventKey)
    for rank in rankings:
        if 'frc' + str(rank.team) == teamKey:
            return rank.rank

    return None


def send_and_get_response(uri):
    request = Request(uri)
    Request.add_header(request, "X-TBA-App-Id", "gamesense:gamesensebot:v02")
    try:
        response_body = urlopen(request).read()
        return response_body
    except HTTPError:
        return None
