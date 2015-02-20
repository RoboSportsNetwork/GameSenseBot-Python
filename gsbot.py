from willie.module import commands, example
from willie import TbaCommunicator as communicator
from datetime import date


@commands('tba')
@example('.tba 319', 'http://www.thebluealliance.com/team/319')
def tba(bot, trigger):
    """Gets the TBA URL for the provided team number"""
    teamNumber = trigger.group(2)
    if teamNumber.isdigit():
        urlbase = 'http://www.thebluealliance.com/team/'
        url = urlbase + teamNumber
        bot.reply(url)
    else:
        bot.reply("ERROR: Invalid team number provided.")


@commands('name')
@example('.name 319', 'Team 319\'s name is Big Bad Bob.')
def name(bot, trigger):
    """Gets the name of the provided team"""
    teamNumber = trigger.group(2)
    team = communicator.getTeam('frc' + teamNumber)
    bot.reply('Team ' + teamNumber + '\'s name is ' + team.nickname + ".")


@commands('record')
@example('.record 319 2014', 'Team 319 was 39-27-1 in 2014.')
def record(bot, trigger):
    """Gets the record of the provided team for the given year"""
    inputs = trigger.group(2).split()

    teamNumber = inputs[0]

    year = 0
    eventCode = 'no_evt'

    if len(inputs) < 2:
        year = '2015'
    elif inputs[1].isdigit():
        year = inputs[1]
    else:
        eventCode = inputs[1]

    if year != 0:
        matches = communicator.getAllTeamMatches('frc' + teamNumber, year)

        if not matches:
            bot.reply(
                str(teamNumber)
                + ' did not play in any matches in '
                + str(year) + '.'
            )
        else:
            bot.reply(
                str(teamNumber) + ' was ' +
                communicator.getTeamRecordInMatches('frc' +
                                                    teamNumber, matches)
                .toString() + ' in ' + str(year) + ".")

    elif eventCode != 'no_evt':
        matches = communicator.getTeamEventMatches(
            'frc' + teamNumber, eventCode)
        event = communicator.getEvent(eventCode)

        if not matches:
            bot.reply(
                str(teamNumber)
                + ' did not play in any matches at '
                + event.name + ' (' + event.event_code + ').'
            )

        else:
            bot.reply(
                str(teamNumber) + ' was ' +
                communicator.getTeamRecordInMatches('frc' +
                                                    teamNumber, matches)
                .toString() + ' at the ' + str(event.year) + ' ' + event.toString() + '.')


@commands('events')
@example('.events 319 2014')
def events(bot, trigger):
    """Gets the list of events the team for the given year"""
    inputs = trigger.group(2).split()

    teamNumber = inputs[0]

    if len(inputs) < 2:
        year = '2015'
    else:
        year = inputs[1]

    reqDate = date(int(year), 1, 1)

    events = communicator.getTeamEvents('frc' + teamNumber, year)

    if not events:
        bot.reply(
            'No events found for ' + str(teamNumber) + ' in ' + str(year) +
            '.')
    else:
        responseString = str(teamNumber)

        if reqDate.year < date.today().year:
            responseString = responseString + ' attended '
        else:
            responseString = responseString + ' is registered for '

        for evt in events:
            responseString = responseString + evt.toString() + ', '

        responseString = responseString[:-2] + " in " + year + '.'

        bot.reply(responseString)


@commands('matchresult')
@example('.matchresult 2014cmp f1m1', 'Red (1678, 1640, 1114) - 236 | Blue (469, 2848, 254) - 361')
def matchresult(bot, trigger):
    """Gets the result of the specified match"""
    inputs = trigger.group(2).split()

    eventCode = inputs[0]
    matchCode = inputs[1]

    if not eventCode[0].isdigit():
        eventCode = '2015' + eventCode

    match = communicator.getMatch(eventCode, matchCode)

    if not match:
        bot.reply("No match results on TBA for that match.")
    else:
        bot.reply(match.getResultString())


@commands('awards')
@example('.awards 2014nhdur', 'Get awards for an entire event.')
@example('.awards 319', 'Get awards for a team in the current year.')
@example('.awards 319 2014', 'Get awards for a team in the given year.')
@example('.awards 319 2014nhdur', 'Get awards for a team at a given event.')
def awards(bot, trigger):
    """Gets awards from TBA's database"""
    inputs = trigger.group(2).split()

    awards_list = []

    if len(inputs) < 2:
        if inputs[0][-1:].isdigit():
            teamKey = inputs[0]
            awards_list = communicator.getTeamYearAwards(
                'frc' + str(teamKey), '2015')
        else:
            eventCode = inputs[0]
            if not eventCode[0].isdigit():
                eventCode = '2015' + eventCode
            awards_list = communicator.getEventAwards(eventCode)
    else:
        if inputs[0][-1:].isdigit() and inputs[1][-1:].isdigit():
            teamKey = inputs[0]
            year = inputs[1]
            awards_list = communicator.getTeamYearAwards(
                'frc' + str(teamKey), str(year))
        else:
            teamKey = inputs[0]
            eventCode = inputs[1]
            if not eventCode[0].isdigit():
                eventCode = '2015' + eventCode
            awards_list = communicator.getTeamEventAwards(
                'frc' + str(teamKey), eventCode)

    response = ''
    if not awards_list:
        response = 'No awards listed.  '
    else:
        for award in awards_list:
            if award:
                response += award.toString() + ', '

    bot.reply("I'm sending you a private message with the awards results.")
    bot.msg(trigger.nick, response[:-2], 5)
