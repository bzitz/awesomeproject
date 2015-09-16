import csv, random, nfldb, json
from stats import Stats 
class Team(object):
    def __init__(self):
        self.qb = ''
        self.rb1 = ''
        self.rb2 = ''
        self.wr1 = ''
        self.wr2 = ''
        self.wr3 = ''
        self.te = ''
        self.flex = ''
        self.dst = ''
        self.team_maxsalary = 50000
        self.ppg = 0
        self.players = {}
        self.team = {}
        self.teamavg = 0
        self.teamsalary = 0
        self.teamvalue = 0
        self.teamtouches = 0

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
            self.target_pergame(i)
            self.players[i]['teamAbbrev'] = self.players[i]['teamAbbrev'].upper()
            stat = Stats()
            self.players[i]['targin20'] = stat.targetin20(i)
            self.players[i]['targin10'] = stat.targetin10(i)
            self.players[i]['percentin20'] = stat.percent_targets(20,self.players[i]['teamAbbrev'],self.players[i]['targin20'])
            self.players[i]['percentin10'] = stat.percent_targets(10,self.players[i]['teamAbbrev'],self.players[i]['targin10'])
            if float(self.players[i]['AvgPointsPerGame']) > 0:
                value = float(self.players[i]['Salary']) / float(self.players[i]['AvgPointsPerGame'])
                self.players[i]['Value'] = value
            else:
                value = 0
                self.players[i]['Value'] = value
    def target_pergame(self, player):
            db = nfldb.connect()
            q = nfldb.Query(db)
            q.game(season_year=2015, season_type='Regular')
            q.player(full_name= player)
            total = 0
            for game in q.as_aggregate():
                total = total + (game.rushing_att + game.receiving_tar)
                #print game.player, (game.rushing_att + game.receiving_tar)/16
            self.players[player]['tchpergame'] = int(total)

    def starting_qbs(self):
#        qbs = ['Tom Brady','Ben Roethlisberger','Tyrod Taylor','Ryan Tannehill','Ryan Fitzpatrick','Joe Flacco', 'Andy Dalton', 'Brian Hoyer', 'Andrew Luck', 'Blake Bortles', 'Marcus Mariota','Peyton Manning', 'Alex Smith', 'Derek Carr', 'Philip Rivers', 'Tony Romo', 'Kirk Cousins', 'Sam Bradford', 'Eli Manning',  'Jay Cutler', 'Matthew Stafford', 'Jay Cutler', 'Aaron Rodgers', 'Teddy Bridgewater', 'Matt Ryan', 'Cam Newton', 'Drew Brees', 'Jameis Winston', 'Carson Palmer', 'Colin Kaepernick', 'Russell Wilson', 'Nick Foles' ]
        qbs = ['Drew Brees','Eli Manning','Carson Palmer','Joe Flacco']
        return qbs
    def add_toteam(self,pos,player):
        self.team[pos] = self.players[player]
        self.team[pos]['Name'] = player
    def pick_qb(self):
        if self.qb == '':
            qbs = self.starting_qbs()
            self.qb = random.choice(qbs)
            self.add_toteam('qb', self.qb)
        else:
            self.add_toteam('qb', self.qb)

    def pick_rbs(self):
        rbs = []
        for i in self.players:
            if self.players[i]['Position'] == "RB" and self.players[i]['tchpergame'] > 13:
                rbs.append(i)
        if self.rb1 == '' and self.rb2 == '':
            picked = random.sample(rbs,2)
            self.rb1 = picked[0]
            self.rb2 = picked[1]
            self.add_toteam('rb1', self.rb1)
            self.add_toteam('rb2', self.rb2)
        elif self.rb1 != '' and self.rb2 == '':
            rbs.remove(self.rb1)
            picked = random.choice(rbs)
            self.rb2 = picked
            self.add_toteam('rb1', self.rb1)
            self.add_toteam('rb2', self.rb2)
        elif self.rb1 == '' and self.rb2 != '':
            rbs.remove(self.rb2)
            picked = random.choice(rbs)
            self.rb1 = picked
            self.add_toteam('rb1', self.rb1)
            self.add_toteam('rb2', self.rb2)
        else:
            self.add_toteam('rb1', self.rb1)
            self.add_toteam('rb2', self.rb2)

    def pick_wrs(self):
        wrs = []
        for i in self.players:
            if self.players[i]['Position'] == "WR" and self.players[i]['tchpergame'] > 3:
                wrs.append(i)
        if self.wr1 == '' and self.wr2 == '' and self.wr3 == '':
            picked = random.sample(wrs,3)
            self.wr1 = picked[0]
            self.wr2 = picked[1]
            self.wr3 = picked[2]
            self.add_toteam('wr1', self.wr1)
            self.add_toteam('wr2', self.wr2)
            self.add_toteam('wr3', self.wr3)
        elif self.wr1 != '' and self.wr2 == '' and self.wr3 == '':
            if self.wr1 in wrs:
                wrs.remove(self.wr1)
            picked = random.sample(wrs,2)
            self.wr2 = picked[0]
            self.wr3 = picked[1]
            self.add_toteam('wr1', self.wr1)
            self.add_toteam('wr2', self.wr2)
            self.add_toteam('wr3', self.wr3)
        elif self.wr1 != '' and self.wr2 != '' and self.wr3 == '':
            if self.wr1 in wrs:
                wrs.remove(self.wr1)
            if self.wr2 in wrs:
                wrs.remove(self.wr2)
            picked = random.choice(wrs)
            self.wr3 = picked
            self.add_toteam('wr1', self.wr1)
            self.add_toteam('wr2', self.wr2)
            self.add_toteam('wr3', self.wr3)
        elif self.wr1 != '' and self.wr2 != '' and self.wr3 != '':
            self.add_toteam('wr1', self.wr1)
            self.add_toteam('wr2', self.wr2)
            self.add_toteam('wr3', self.wr3)

    def pick_te(self):
        tes = []
        for i in self.players:
            if self.players[i]['Position'] == "TE" and self.players[i]['tchpergame'] > 2:
                tes.append(i)
        if self.te == '':
            self.te = random.choice(tes)
            self.add_toteam('te', self.te)
        else:
            self.add_toteam('te', self.te)

    def pick_flex(self):
        if self.flex != '':
            self.add_toteam('flex',self.flex)
        else:
            flex = []
            pos = self.players
            for i in pos:
                if (pos[i]['Position'] == "TE" or pos[i]['Position'] == "RB" or pos[i]['Position'] == "WR") and self.players[i]['tchpergame'] > 7:
                    flex.append(i)
            rmlist = [self.rb1,self.rb2,self.wr1,self.wr2,self.wr3,self.te]
            for x in rmlist:
                if x in flex:
                    flex.remove(x)
            self.flex = random.choice(flex)
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
    def team_salary(self):
        positions = self.return_pos()
        salary = 0
        for x in positions:
            salary = salary + int(self.team[x]['Salary'])
        self.teamsalary = salary
    def team_avg_score(self):
        positions = self.return_pos()
        avgpergame = 0
        for x in positions:
            avgpergame = avgpergame + float(self.team[x]['AvgPointsPerGame'])
        self.teamavg = avgpergame 

    def main(self):
        self.import_json()
        self.pick_team()
        self.team_value()
        self.team_salary()
        self.team_avg_score()
        self.team_touches()
        

#new = Team()
#
#new.import_data()
#new.add_value()
#new.pick_team()
#print new.qb, new.players[new.qb]['Value']
#print new.rb1
#print new.rb2
#print new.wr1
#print new.wr2
#print new.wr3
#print new.te
#print new.flex
#print new.team
#print new.team_value()
#print new.team_salary()
#print new.team_avg_score()

