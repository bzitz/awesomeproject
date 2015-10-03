import csv, random, nfldb, json, stats
from stats import Stats 

class Player(object):
    def __init__(self, position):
        self.position = position
        self.players = {}
        self.offensepositions = ['QB','RB','WR','TE']
        self.qbs = []
        self.rb1s = []
        self.rb2s = []
        self.wr1s = []
        self.wr2s = []
        self.wr3s = []
        self.flexlist = []
        self.tes = []
        self.dst  = []

    def pick_flex(self,wr1,wr2,wr3,te):
        flex = []
        flex5 = []
        self.import_json()
        pos = self.players
        for i in pos:
            if (pos[i]['Position'] == "TE" or pos[i]['Position'] == "WR") and self.players[i]['Overallrank'] < 40:
                flex.append(i)

        rmlist = [wr1,wr2,wr3,te]
        for x in rmlist:
            if x in flex:
                flex.remove(x)
        for y in flex[:5]:
            self.flexlist.append(y)
            flex5.append(y)
        return flex5

    def get_pos(self):
        self.import_json()
        s = stats.Stats()
        for pos in self.offensepositions:
            if pos == 'QB':
                for x in self.top_players('QB',1):
                    self.qbs.append(x[0])
            if pos == 'RB':
                print "POS: ", pos
                rbs = self.top_players('RB', 10)
                for x in rbs[:5]:
                    self.rb1s.append( x[0] )
                for x in rbs[-5:]:
                    self.rb2s.append( x[0] )
            if pos == 'WR':
                wrs = self.top_players('WR', 15)
                for x in wrs[:5]:
                    self.wr1s.append( x[0] )
                for y in wrs[5:10]:
                    self.wr2s.append( y[0] )
                for z in wrs[-5:]:
                    self.wr3s.append( z[0] )
            if pos == 'TE':
                for x in self.top_players('TE', 10):
                    self.tes.append(x[0])


    
    def import_json(self):
        jsonfile = open('dkplayers.json', "r")
        self.players = json.load(jsonfile)

    def update_ptsperopp(self):
        for i in self.players:
            if self.players[i]['Position'] != 'DST':
                if self.players[i]['AvgPointsPerGame'] == 0 or self.players[i]['Oppscore'] == 0:
                    self.players[i]['PtsPerOpp'] = 0
                else:
                    self.players[i]['PtsPerOpp'] = float("{0:.2f}".format(float(self.players[i]['AvgPointsPerGame'])/float(self.players[i]['Oppscore'])))
    def startingqbs(self):
        qbs = ['Tom Brady','Ben Roethlisberger','Tyrod Taylor','Ryan Tannehill','Ryan Fitzpatrick','Joe Flacco', 'Andy Dalton', 'Brian Hoyer', 'Andrew Luck', 'Blake Bortles', 'Marcus Mariota','Derek Carr', 'Philip Rivers', 'Tony Romo', 'Kirk Cousins', 'Sam Bradford', 'Eli Manning',  'Jay Cutler', 'Matthew Stafford', 'Jay Cutler', 'Aaron Rodgers', 'Teddy Bridgewater', 'Matt Ryan', 'Cam Newton', 'Drew Brees', 'Jameis Winston', 'Carson Palmer', 'Colin Kaepernick', 'Russell Wilson', 'Nick Foles' ]
        return qbs

    # Ranks a position by a statistic
    def rank_players(self, pos, stat):
        stats = []
        playerlst = []
        if pos !='DST':
            for x in self.players:
                if self.players[x]['Position'] == pos:
                    playerlst.append(x)
                    
        for x in playerlst:
            stats.append( (x,self.players[x][stat]) )
            if stat == 'Overall':
                sortedstats = sorted(stats,key=lambda tup: tup[1])
            else:
                sortedstats = sorted(stats,key=lambda tup: tup[1],reverse=True)
        rank = 1
        for x in sortedstats:
            self.players[x[0]][stat+'rank'] = rank
            rank = rank + 1

    def update_ranks(self):
        stats = ['Oppscore','PtsPerOpp']
        for y in self.offensepositions:
            for x in stats:
                self.rank_players(y,x)
    
    def player_rating(self):
        for y in self.players:
            if self.players[y]['Position'] != 'DST':
                print y
                self.players[y]['Overall'] = float("{0:.2f}".format((self.players[y]['Oppscorerank'] * .95) + (self.players[y]['PtsPerOpprank'] * .05)))
        positions = ['QB','RB','WR','TE']
        for y in positions:
            self.rank_players(y,'Overall')
    
    def top_players(self,pos,num):
        s = stats.Stats()
        return s.top_oppscore(self.players,pos,num)
    
    
class Team(object):
    def __init__(self,qb,rb1,rb2,wr1,wr2,wr3,te,flex,dst):
        self.qb = qb
        self.rb1 = rb1 
        self.rb2 = rb2
        self.wr1 = wr1 
        self.wr2 = wr2 
        self.wr3 = wr3 
        self.te = te
        self.flex = flex
        self.dst = dst
        self.team_maxsalary = 50000
        self.ppg = 0
        self.players = {} 
        self.team = {}
        self.teamavg = 0
        self.teamsalary = 0
        self.teamvalue = 0
        self.teamtouches = 0
        self.teamtch20 = 0
        self.teamtch10 = 0
        self.teamopp = 0
        self.teamoverallrank = 0
        self.selected = []
        self.flexlist = []

    def remove_zeros(self):
        nonzeros = {}
        for x in self.players:
            if self.players[x]['Value'] > 0:
                nonzeros[x] = self.players[x]
        self.players = nonzeros
    def import_json(self):
        jsonfile = open('dkplayers.json', "r")
        self.players = json.load(jsonfile)

    def import_data(self):
        reader = csv.DictReader(open('DKSalaries.csv'))
        for row in reader:
            key = row.pop('Name')
            self.players[key] = row
    
    def add_value(self):
        for i in self.players:
            self.players[i]['teamAbbrev'] = self.players[i]['teamAbbrev'].upper()
            stat = Stats()
            if float(self.players[i]['AvgPointsPerGame']) > 0:
                value = float(self.players[i]['Salary']) / float(self.players[i]['AvgPointsPerGame'])
                self.players[i]['Value'] = value
            else:
                value = 0
                self.players[i]['Value'] = value
            if self.players[i]['Position'] != 'QB' and self.players[i]['Position'] != 'DST':
                if stat.flexoppurtunity_index(i,2015) == 0:
                    self.players[i]['Oppscore'] = 0
                else:
                    self.players[i]['Oppscore'] = stat.flexoppurtunity_index(i,2015) / stat.games_played(i,2015)
            if self.players[i]['Position'] == 'QB':
                if stat.qboppurtunity(i,2015) == 0:
                    self.players[i]["Oppscore"] = 0
                else:
                    self.players[i]['Oppscore'] = stat.qboppurtunity(i,2015) / stat.games_played(i,2015)
                print i, self.players[i]['Oppscore']

    def starting_qbs(self):
        qbs = ['Tom Brady','Ben Roethlisberger','Tyrod Taylor','Ryan Tannehill','Ryan Fitzpatrick','Joe Flacco', 'Andy Dalton', 'Brian Hoyer', 'Andrew Luck', 'Blake Bortles', 'Marcus Mariota','Derek Carr', 'Philip Rivers', 'Tony Romo', 'Sam Bradford',  'Jay Cutler', 'Matthew Stafford', 'Jay Cutler', 'Aaron Rodgers', 'Teddy Bridgewater', 'Matt Ryan', 'Cam Newton', 'Drew Brees', 'Jameis Winston', 'Carson Palmer', 'Colin Kaepernick', 'Russell Wilson', 'Nick Foles' ]
        #qbs = ['Ben Roethlisberger','Drew Brees','Eli Manning','Carson Palmer','Joe Flacco']
        return qbs

    def add_toteam(self,pos,player):
        self.team[pos] = self.players[player]
        self.team[pos]['Name'] = player

    def pick_qb(self):
        self.add_toteam('qb', self.qb)

    def pick_rbs(self):
        self.add_toteam('rb1', self.rb1)
        self.add_toteam('rb2', self.rb2)

    def pick_wrs(self):
        self.add_toteam('wr1', self.wr1)
        self.add_toteam('wr2', self.wr2)
        self.add_toteam('wr3', self.wr3)

    def pick_te(self):
        self.add_toteam('te', self.te)

    def pick_flex(self):
        self.add_toteam('flex',self.flex) 
   
    
    def pick_dst(self):
        if self.dst != '':
            self.add_toteam('dst', self.dst)
        else:
            dst = []
            for i in self.players:
                if self.players[i]['Position'] == "DST":
                    dst.append(i)
            self.dst = random.choice(dst)
            self.add_toteam('dst',self.dst)

    def pick_team(self):
        self.pick_qb()
        self.pick_rbs()
        self.pick_wrs()
        self.pick_te()
        self.pick_flex()
        self.pick_dst()

    def get_value(self, player):
        value = self.players[player]['AvgPointsPerGame']
        return value
    def get_price(self, player):
        value = self.players[player]['Salary']
        return value
    def return_pos(self):
        positions = ['qb','rb1','rb2','wr1','wr2','wr3','te','flex','dst']
        return positions
    def team_touches(self):
        positions = self.return_pos()
        value = 0
        for x in positions:
            if x != 'dst':
                value = value + self.team[x]['tchpergame']
        self.teamtouches = value
        self.team['Targets'] = self.teamtouches 
    def team_value(self):
        positions = self.return_pos()
        value = 0
        for x in positions:
            value = value + self.team[x]['Value']
        self.teamvalue = value
        self.team['Value'] = self.teamvalue
    def team_salary(self):
        positions = self.return_pos()
        salary = 0
        for x in positions:
            salary = salary + int(self.team[x]['Salary'])
        self.teamsalary = salary
        self.team['TeamSalary'] = self.teamsalary
    def team_avg_score(self):
        positions = self.return_pos()
        avgpergame = 0
        for x in positions:
            avgpergame = avgpergame + float(self.team[x]['AvgPointsPerGame'])
        self.teamavg = avgpergame 
        self.team['Teamppg'] = self.teamavg
    def team_tch20(self):
        positions = self.return_pos()
        tch20 = 0
        for x in positions:
            tch20 = tch20 + self.team[x]['targin20']
        self.teamtch20 = tch20
        self.team['TeamTch20'] = self.teamtch20
    def team_tch10(self):
        positions = self.return_pos()
        tch10 = 0
        for x in positions:
            tch10 = tch10 + self.team[x]['targin10']
        self.teamtch10 = tch10
        self.team['TeamTch10'] = self.teamtch10
    def team_opp(self):
        opp = 0
        pos = self.return_pos()
        for x in pos:
            if x != 'dst':
                opp = opp + self.team[x]['Oppscore']
        self.teamopp = opp
        self.team['Oppscore'] = self.teamopp
    def team_overall(self):
        opp = 0
        pos = self.return_pos()
        for x in pos:
            if x != 'dst':
                opp = opp + self.team[x]['Overallrank']
        self.teamoverallrank = opp
        self.team['Overallrank'] = float(self.teamoverallrank) / float('8.000')
    def team_ppo(self):
        ppo = self.teamavg / self.teamopp
        self.team['PPO'] = ppo


    def main(self):
        self.import_json()
        self.pick_team()
        self.team_value()
        self.team_salary()
        self.team_avg_score()
        self.team_opp()
        self.team_overall()
        self.team_ppo()
    def get_teamstat(self):
        self.team_value()
        self.team_salary()
        self.team_avg_score()
        self.team_opp()
        self.team_overall()
        self.team_ppo()

