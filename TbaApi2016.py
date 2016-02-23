class TbaTeam:

    def __init__(self):
        self.website = ''
        self.name = ''
        self.locality = ''
        self.region = ''
        self.country = ''
        self.location = ''
        self.team_number = 0
        self.key = ''
        self.nickname = ''
        self.rookie_year = 0

    def deserialize(self, json_obj):
        self.website = json_obj.get('website')
        self.name = json_obj.get('name')
        self.locality = json_obj.get('locality')
        self.region = json_obj.get('region')
        self.country = json_obj.get('country')
        self.location = json_obj.get('location')
        self.team_number = json_obj.get('team_number')
        self.key = json_obj.get('key')
        self.nickname = json_obj.get('nickname')
        self.rookie_year = json_obj.get('rookie_year')
        return self


class TbaEvent:

    def __init__(self):
        self.key = ''
        self.website = ''
        self.official = False
        self.end_date = ''
        self.name = ''
        self.short_name = ''
        self.facebook_eid = ''
        self.event_district_string = ''
        self.venue_address = ''
        self.event_district = 0
        self.location = ''
        self.event_code = ''
        self.year = 0
        self.webcast = []
        self.alliances = []
        self.event_type_string = ''
        self.start_date = ''
        self.event_type = 0

    def deserialize(self, json_obj):
        self.key = json_obj.get('key')
        self.website = json_obj.get('website')
        self.official = json_obj.get('official')
        self.end_date = json_obj.get('end_date')
        self.name = json_obj.get('name')
        self.short_name = json_obj.get('short_name')
        self.facebook_eid = json_obj.get('facebook_eid')
        self.event_district_string = json_obj.get('event_district_string')
        self.venue_address = json_obj.get('venue_address')
        self.event_district = json_obj.get('event_district')
        self.location = json_obj.get('location')
        self.event_code = json_obj.get('event_code')
        self.year = json_obj.get('year')

        webcast_dictionary_list = json_obj.get('webcast')
        for item in webcast_dictionary_list:
            wc = TbaWebcast()
            wc.deserialize(item)
            self.webcast.append(wc)

        alliances_dictionary_list = json_obj.get('alliances')
        for item in alliances_dictionary_list:
            alliance = TbaAlliance()
            alliance.deserialize(item)
            self.alliances.append(alliance)

        self.event_type_string = json_obj.get('event_type_string')
        self.start_date = json_obj.get('start_date')
        self.event_type = json_obj.get('event_type')
        return self

    def toString(self):
        return self.name + ' (' + self.event_code + ')'


class TbaWebcast:

    def __init__(self):
        self.type = ''
        self.channel = ''

    def deserialize(self, json_obj):
        self.type = json_obj.get('type')
        self.channel = json_obj.get('channel')
        return self


class TbaAlliance:

    def __init__(self):
        self.score = 0
        self.teams = []

    def deserialize(self, json_obj):
        self.score = json_obj.get('score')

        teams_dictionary_list = json_obj.get('teams')

        if not teams_dictionary_list:
            return self
        else:
            for item in teams_dictionary_list:
                self.teams.append(item)

            return self


class TbaTeamRecord:

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def toString(self):
        return str(self.wins) + '-' + str(self.losses) + '-' + str(self.ties)

class TbaTeamScoreAvg:

    def __init__(self):
        self.qualAvg = 0
        self.playoffAvg = 0

    def toString(self):
        return 'Qual: ' + str(self.qualAvg) + ', Playoff: ' + str(self.playoffAvg)

class TbaMatch:

    def __init__(self):
        self.comp_level = ''
        self.match_number = ''
        self.videos = []
        self.set_number = ''
        self.key = ''
        self.time = ''
        self.score_breakdown = TbaScoreBreakDown()
        self.alliances = TbaAlliances()
        self.event_key = ''

    def deserialize(self, json_obj):
        self.comp_level = json_obj.get('comp_level')
        self.match_number = json_obj.get('match_number')

        videos_dictionary_list = json_obj.get('videos')
        for item in videos_dictionary_list:
            vid = TbaVideo()
            vid.deserialize(item)
            self.videos.append(vid)

        self.set_number = json_obj.get('set_number')
        self.key = json_obj.get('key')
        self.time = json_obj.get('time')
        self.score_breakdown.deserialize(json_obj.get('score_breakdown'))
        self.alliances.deserialize(json_obj.get('alliances'))
        self.event_key = json_obj.get('event_key')
        return self

    def getResultString(self):
        blue1 = self.alliances.blue.teams[0]
        blue2 = self.alliances.blue.teams[1]
        blue3 = self.alliances.blue.teams[2]

        red1 = self.alliances.red.teams[0]
        red2 = self.alliances.red.teams[1]
        red3 = self.alliances.red.teams[2]

        blueTeams = blue1[3:] + ', ' + blue2[3:] + ', ' + blue3[3:]
        redTeams = red1[3:] + ', ' + red2[3:] + ', ' + red3[3:]

        return 'Blue(' + blueTeams + ') - ' + str(self.alliances.blue.score) + \
            ' | ' + str(self.alliances.red.score) + \
            ' - Red(' + redTeams + ')'


class TbaAlliances:

    def __init__(self):
        self.blue = TbaAlliance()
        self.red = TbaAlliance()

    def deserialize(self, json_obj):
        self.blue.deserialize(json_obj.get('blue'))
        self.red.deserialize(json_obj.get('red'))
        return self


class TbaAllianceScoreBreakdown:

    def __init__(self):
        self.teleopPoints = 0
        self.robot3Auto = ''
        self.breachPoints = 0
        self.autoPoints = 0
        self.teleopScalePoints = 0
        self.autoBouldersLow = 0
        self.teleopTowerCaptured = ''
        self.teleopBouldersLow = 0
        self.teleopCrossingPoints = 0
        self.foulCount = 0
        self.foulPoints = 0
        self.towerFaceB = ''
        self.towerFaceC = ''
        self.towerFaceA = ''
        self.techFoulCount = 0
        self.totalPoints = 0
        self.adjustPoints = 0
        self.position3 = ''
        self.robot1Auto = ''
        self.position4 = ''
        self.position5 = ''
        self.autoBoulderPoints = 0
        self.teleopBoulderPoints = 0
        self.teleopBouldersHigh = 0
        self.autoBouldersHigh = 0
        self.robot2Auto = ''
        self.position1crossings = 0
        self.towerEndStrength = 0
        self.position4crossings = 0
        self.position2crossings = 0
        self.position5crossings = 0
        self.position3crossings = 0
        self.teleopChallengePoints = 0
        self.autoCrossingPoints = 0
        self.teleopDefensesBreached = ''
        self.autoReachPoints = 0
        self.position2 = ''
        self.capturePoints = 0

    def deserialize(self, json_obj):
        self.teleopPoints = json_obj.get('teleopPoints')
        self.robot3Auto = json_obj.get('robot3Auto')
        self.breachPoints = json_obj.get('breachPoints')
        self.autoPoints = json_obj.get('autoPoints')
        self.teleopScalePoints = json_obj.get('teleopScalePoints')
        self.autoBouldersLow = json_obj.get('autoBouldersLow')
        self.teleopTowerCaptured = json_obj.get('teleopTowerCaptured')
        self.teleopBouldersLow = json_obj.get('teleopBouldersLow')
        self.teleopCrossingPoints = json_obj.get('teleopCrossingPoints')
        self.foulCount = json_obj.get('foulCount')
        self.foulPoints = json_obj.get('foulPoints')
        self.towerFaceB = json_obj.get('towerFaceB')
        self.towerFaceC = json_obj.get('towerFaceC')
        self.towerFaceA = json_obj.get('towerFaceA')
        self.techFoulCount = json_obj.get('techFoulCount')
        self.totalPoints = json_obj.get('totalPoints')
        self.adjustPoints = json_obj.get('adjustPoints')
        self.position3 = json_obj.get('position3')
        self.robot1Auto = json_obj.get('robot1Auto')
        self.position4 = json_obj.get('position4')
        self.position5 = json_obj.get('position5')
        self.autoBoulderPoints = json_obj.get('autoBoulderPoints')
        self.teleopBoulderPoints = json_obj.get('teleopBoulderPoints')
        self.teleopBouldersHigh = json_obj.get('teleopBouldersHigh')
        self.autoBouldersHigh = json_obj.get('autoBouldersHigh')
        self.robot2Auto = json_obj.get('robot2Auto')
        self.position1crossings = json_obj.get('position1crossings')
        self.towerEndStrength = json_obj.get('towerEndStrength')
        self.position4crossings = json_obj.get('position4crossings')
        self.position2crossings = json_obj.get('position2crossings')
        self.position5crossings = json_obj.get('position5crossings')
        self.position3crossings = json_obj.get('position3crossings')
        self.teleopChallengePoints = json_obj.get('teleopChallengePoints')
        self.autoCrossingPoints = json_obj.get('autoCrossingPoints')
        self.teleopDefensesBreached = json_obj.get('teleopDefensesBreached')
        self.autoReachPoints = json_obj.get('autoReachPoints')
        self.position2 = json_obj.get('position2')
        self.capturePoints = json_obj.get('capturePoints')
        return self


class TbaScoreBreakDown:

    def __init__(self):
        self.blue = TbaAllianceScoreBreakdown()
        self.red = TbaAllianceScoreBreakdown()

    def deserialize(self, json_obj):
        if not json_obj:
            return self
        else:
            self.blue.deserialize(json_obj.get('blue'))
            self.red.deserialize(json_obj.get('red'))
        return self


class TbaVideo:

    def __init__(self):
        self.video_type = ''
        self.key = ''

    def deserialize(self, json_obj):
        self.video_type = json_obj.get('type')
        self.key = json_obj.get('key')
        return self


class TbaAward:

    def __init__(self):
        self.event_key = ''
        self.award_type = 0
        self.name = ''
        self.recipient_list = []
        self.year = 0

    def deserialize(self, json_obj):
        self.event_key = json_obj.get('event_key')
        self.award_type = json_obj.get('award_type')
        self.name = json_obj.get('name')

        recipient_dictionary_list = json_obj.get('recipient_list')
        for item in recipient_dictionary_list:
            recipient = TbaAwardRecipient()
            recipient.deserialize(item)
            self.recipient_list.append(recipient)

        self.year = json_obj.get('year')

        return self

    def toString(self):
        recipientString = '('

        for recip in self.recipient_list:
            if not recip.awardee:
                recipientString += str(recip.team_number)
            elif not recip.team_number:
                recipientString += recip.awardee
            else:
                recipientString += recip.awardee + \
                    '(' + str(recip.team_number) + ')'
            recipientString += ', '
        recipientString = recipientString[:-2] + ')'

        return self.name + ' ' + recipientString


class TbaAwardRecipient:

    def __init__(self):
        self.team_number = 0
        self.awardee = ''

    def deserialize(self, json_obj):
        self.team_number = json_obj.get('team_number')
        self.awardee = json_obj.get('awardee')
        return self


class Tba2016Ranking:

    def __init__(self):
        self.rank = 0
        self.team = 0
        self.ranking_score = 0.0
        self.auto = 0
        self.scale_challenge = 0
        self.goals = 0
        self.defense = 0
        self.record = 0
        self.played = 0

    def deserialize(self, json_obj):
        self.rank = json_obj[0]
        self.team = json_obj[1]
        self.ranking_score = json_obj[2]
        self.auto = json_obj[3]
        self.scale_challenge = json_obj[4]
        self.goals = json_obj[5]
        self.defense = json_obj[6]
        self.record = json_obj[7]
        self.played = json_obj[8]

    def toString(self):
        return str(self.rank) + '. ' + str(self.team) + ' (' + str(self.record) + ') | '