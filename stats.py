import nfldb
class Stats(object):
    def __init__(self):
        self.targets = 0
        self.in20targets = 0
        self.in10targets = 0
        self.teamin20targets = 0
        self.teamin10targets =0


    def target_pergame(self, player):
        db = nfldb.connect()
        q = nfldb.Query(db)
        q.game(season_year=2015, season_type='Regular')
        q.player(full_name= player)
        total = 0
        for game in q.as_aggregate():
            total = total + (game.rushing_att + game.receiving_tar)
        return int(total)
    
    def targetin20(self, player):
        db = nfldb.connect()
        q = nfldb.Query(db)
        opp20 = nfldb.FieldPosition.from_str('OPP 20')
        q.game(season_year=2015, season_type='Regular')
        q.play(yardline__ge=opp20)
        q.player(full_name = player)
        total = 0
        for game in q.as_aggregate():
            total = total + (game.rushing_att + game.receiving_tar)
        return int(total)
            
    def targetin10(self, player):
        db = nfldb.connect()
        q = nfldb.Query(db)
        opp20 = nfldb.FieldPosition.from_str('OPP 10')
        q.game(season_year=2015, season_type='Regular')
        q.play(yardline__ge=opp20)
        q.player(full_name = player)
        total = 0
        for game in q.as_aggregate():
            total = total + (game.rushing_att + game.receiving_tar)
        return int(total)

    def teamtargetin20(self, team):
        db = nfldb.connect()
        q = nfldb.Query(db)
        opp20 = nfldb.FieldPosition.from_str('OPP 20')
        q.game(season_year=2015, season_type='Regular')
        q.play(yardline__ge=opp20, pos_team = team)
        return len(q.as_plays())
    
    def teamtargetin10(self, team):
        db = nfldb.connect()
        q = nfldb.Query(db)
        opp20 = nfldb.FieldPosition.from_str('OPP 10')
        q.game(season_year=2015, season_type='Regular')
        q.play(yardline__ge=opp20, pos_team = team)
        return len(q.as_plays())
            
    def percent_targets(self, yard, team, player):
        if yard == 20:
            if team != 0 and player != 0:
                print "20", team, player
                percent = (float(player) / float(self.teamtargetin20(team))) * 100
                print int(percent)
            else: 
                percent = 0
        elif yard == 10: 
            if team != 0 and player != 0:
                print "10",team, player
                percent = (float(player) / float(self.teamtargetin10(team))) * 100
                print percent
            else:
                percent = 0
        return int(percent)
        


        
