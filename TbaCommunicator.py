import TbaApi2016 as api
import TbaApiSettings
#from TheBlueAlliance import *
import urllib2, json, time, pickle, operator

timestamp = time.time()
ims_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(timestamp))
api_request_times = {"placeholder": ims_time}

def save_api_request_times():
    out = open( "cache\\" + convertUriToFileName("api_request_times", '.p') , 'wb+' )
    pickle.dump(api_request_times, out)
    out.close()

def load_api_request_times():
    fin = open( "cache\\" + convertUriToFileName("api_request_times", '.p') , 'rb' )
    temp = pickle.load(fin)
    fin.close()
    return temp


def getTeam(teamKey):
    url = TbaApiSettings.tbaBaseUrl + '/team/' + str(teamKey)
    api_response_string = send_and_get_response(url)
    #print "API Response:" + api_response_string
    json_obj = json.loads(api_response_string)
    team = api.TbaTeam()
    return team.deserialize(json_obj)


def getEvent(eventKey):
    url = TbaApiSettings.tbaBaseUrl + '/event/' + str(eventKey)
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    event = api.TbaEvent()
    return event.deserialize(json_obj)


def get_events(year):
    url = TbaApiSettings.tbaBaseUrl + '/events/' + str(year)
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    events = []
    for item in json_obj:
        event = api.TbaEvent()
        event.deserialize(item)
        events.append(event)

    return events


def get_event_teams(event_key):
    url = TbaApiSettings.tbaBaseUrl + '/event/' + event_key + '/teams'
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    teams = []
    for item in json_obj:
        team = api.TbaTeam()
        team.deserialize(item)
        teams.append(team)

    return teams


def get_event_team_count(event_key):
    url = TbaApiSettings.tbaBaseUrl + '/event/' + event_key + '/teams'
    api_response_string = send_and_get_response(url)
    json_obj = json.loads(api_response_string)
    return len(json_obj)


def get_biggest_event(year):
    events = get_events(year)
    biggest_event_team_count = 0
    biggest_event = api.TbaEvent()

    for event in events:
        event_key = event.key
        #print "getting size of " + event_key
        team_count = get_event_team_count(event_key)
        if team_count > biggest_event_team_count:
            biggest_event_team_count = team_count
            biggest_event = event

    return biggest_event, biggest_event_team_count


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
    #print 'event_awards_request: ' + url
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


def get_most_awards(award_name):
    events = get_events(2008)
    events.extend(get_events(2009))
    events.extend(get_events(2010))
    events.extend(get_events(2011))
    events.extend(get_events(2012))
    events.extend(get_events(2013))
    events.extend(get_events(2014))
    events.extend(get_events(2015))

    award_counts = {0: 0}

    for event in events:
        print 'Getting event awards for ' + str(event.year) + event.event_code
        awards = getEventAwards(str(event.year) + event.event_code)
        if awards:
            for award in awards:
                if award_name in award.name:
                    if award_counts.has_key(award.recipient_list[0].team_number):
                        award_counts[award.recipient_list[0].team_number] += 1
                    else:
                        award_counts[award.recipient_list[0].team_number] = 1

    team_num = max(award_counts.iteritems(), key=operator.itemgetter(1))[0]

    return team_num, award_counts[team_num] 



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


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """

    print "I should be printing the request"
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def send_and_get_response(uri):
    api_request_times = load_api_request_times()
    picklable = {uri: 'placeholder'}
    request = urllib2.Request(uri)
    #print "Requesting: " + uri
    request.add_header("X-TBA-App-Id", "gamesense:gamesensebot:v03")
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0" )
    timestamp = time.time()
    ims_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(timestamp))
    if api_request_times.has_key(uri):
        request.add_header("If-Modified-Since", api_request_times[uri])
        save_api_request_times()
        #print "Using If-Modified-Since: " + ims_time
    #prepared = request.prepare()
    #pretty_print_POST(prepared)
    try:
        response_body = urllib2.urlopen(request).read()
        api_request_times[uri] = ims_time
        picklable[uri] = response_body
        out = open( "cache\\" + convertUriToFileName(uri, '.p') , 'wb+' )
        pickle.dump(picklable, out)
        out.close()
        return response_body
    except urllib2.HTTPError, err:
        if err.code == 304:
            #print "API Not Modified.  Reading from cache."
            pickle_in = open( "cache\\" + convertUriToFileName(uri, '.p') , 'rb' )
            picklable = pickle.load(pickle_in)
            pickle_in.close()
            return picklable[uri]
        else:                
            #log_error(detail)
            print err
            return None


def log_error(error_str):
    with open("C:\\Users\\ttremblay\\Documents\\errors.txt", "a+") as myfile:
      myfile.write(error_str)

def convertUriToFileName(uri, fileExtension):
    return uri.replace('/','').replace(':','').replace('.','') + fileExtension;