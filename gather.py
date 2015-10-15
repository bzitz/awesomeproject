import csv, json, os, test
from tabulate import tabulate


jsonfile = open('teamlogs/topteams.json', 'r')
teams = json.load(jsonfile)
gathered = []
totalopp = 0

qb = [
    'Tom Brady', 
    'Aaron Rodgers',
    'Sam Bradford',
    'Philip Rivers',
    'Carson Palmer', 
    'Jay Cutler',
    'Blake Bortles', 
    'Matt Ryan',
    'Marcus Mariota'
 
    ]
rb1 = [
    "Le'Veon Bell",
    'Jamaal Charles',
    'Matt Forte',
    'Latavius Murray',
    'Devonta Freeman']
rb2 = [
    'Justin Forsett',
    'Dion Lewis',
    'LeGarrette Blount',
    'Karlos Williams',
    'Todd Gurley',
    'Doug Martin',
    'C.J. Anderson'
    ]
wr1 = [
    'Julio Jones',
    'Odell Beckham',
    'Larry Fitzgerald',
    'Keenan Allen',
    'Julian Edelman',
    'Demaryius Thomas'
    ]
wr2 = [
    'Jeremy Maclin',
    'Allen Hurns',
    'Amari Cooper',
    'Michael Crabtree',
    'Kendall Wright'
    ]
wr3 = [
    'Leonard Hankerson',
    'Pierre Garcon',
    'Terrance Williams',
    'Doug Baldwin',
    'Martavis Bryant',
    'Eddie Royal'
    ]
te = ['Rob Gronkowski', 'Jordan Reed', 'Travis Kelce','Antonio Gates','Owen Daniels', 'Martellus Bennett']
dsts = ['Bengals ', 'Cardinals ', 'Chiefs ', 'Giants ', 'Bears ', 'Jaguars ']
allplayers = qb + rb1 + rb2 + wr1 + wr2 + wr3 + te

def get_stacked(teamlst,qblst):
    stacked = []
    for x in teamlst:
        for z in qblst:
            if x['qb']['Name'] == z:
                if x['wr1']['teamAbbrev'] == x['qb']['teamAbbrev'] or x['wr2']['teamAbbrev'] == x['qb']['teamAbbrev'] or x['wr3']['teamAbbrev'] == x['qb']['teamAbbrev']:
                    if wrwrcheck(x) and rbqbcheck(x):
                        stacked.append(x)
    return stacked

#get one stacked lineup containing each player
def get_beststacked(teamlst,qb,rb,wr,te):
    allplayers = qb + rb + wr + te
    positions = ['qb','rb1','rb2','wr1','wr2','wr3','te','flex']
    best_lineups = []
    plyer_cnt = {}
    srtlst = sorted(teamlst, key = lambda k: k['Teamppg'], reverse=True)
    for p in allplayers:
        plyer_cnt[p] = 0
    for t in srtlst: 
        tp = []
        cnt = []
        for pos in positions:
            tp.append(t[pos]['Name'])
        for x in tp:
            plyer_cnt[x] = plyer_cnt[x] + 1
            cnt.append(plyer_cnt[x])
        if sorted(cnt,reverse=True)[0] < 20:
            if rbqbcheck(t) and wrwrcheck(t):
                best_lineups.append(t)
        if rbqbcheck(t) and wrwrcheck(t) and excluderb(t,"Devonta Freeman") and excludewr(t,"Michael Crabtree"):
            if t['Oppscore'] > 190:
                best_lineups.append(t)
        if rbqbcheck(t) and wrwrcheck(t) and excluderb(t,"Devonta Freeman") and excludewr(t,"Michael Crabtree") and excludeqb(t,"Blake Bortles") and excludeqb(t,"Derek Carr"):
            if t['Oppscore'] > 170:
                best_lineups.append(t)
    return sorted(best_lineups, key = lambda k: k['Oppscore'], reverse=True) 

def rbqbcheck(lineup):
    if lineup['qb']['teamAbbrev'] != lineup['rb1']['teamAbbrev'] and lineup['qb']['teamAbbrev'] !=  lineup['rb2']['teamAbbrev']:
        return True

def teflexcheck(lineup):
    if lineup['te']['Name'] != lineup['flex']['Name']:
        return True
def wrwrcheck(lineup):
    if lineup['wr1']['teamAbbrev'] != (lineup['wr2']['teamAbbrev'] or lineup['wr3']['teamAbbrev']):
        if lineup['wr2']['teamAbbrev'] != (lineup['wr1']['teamAbbrev'] or lineup['wr3']['teamAbbrev']):
            if lineup['wr3']['teamAbbrev'] != (lineup['wr1']['teamAbbrev'] or lineup['wr2']['teamAbbrev']):
                return True

def wrrbcheck(lineup):
    if lineup['rb1']['teamAbbrev'] != (lineup['wr1']['teamAbbrev'] or lineup['wr2']['teamAbbrev'] or lineup['wr2']['teamAbbrev']):
        if lineup['rb2']['teamAbbrev'] != (lineup['wr1']['teamAbbrev'] or lineup['wr2']['teamAbbrev'] or lineup['wr2']['teamAbbrev']):
            return True

def teamcheck(lineup):
    if rbqbcheck(lineup):
        if wrwrcheck(lineup):
            if wrrbcheck(lineup):
                if teflexcheck(lineup):
                    return True
    
def excludeqb(lineup,name):
    if lineup['qb']['Name'] != name:
        return True
def excluderb(lineup,name):
    if lineup['rb1']['Name'] != name  and lineup['rb2']['Name'] != name:
        return True
def excludewr(lineup,name):
    if lineup['wr1']['Name'] != name  and lineup['wr2']['Name'] != name and lineup['wr3']['Name'] != name and lineup['flex']['Name'] != name:
        return True
def includewr(lineup,name):
    if lineup['wr1']['Name'] == name or lineup['wr2']['Name'] == name and lineup['wr3']['Name'] == name and lineup['flex']['Name'] != name:
        return True
            
def distribution(lineuplist,players):
    positions = ['qb','rb1','rb2','wr1','wr2','wr3','te','flex']
    roster = []
    player_cnt = {}
    for p in players:
        player_cnt[p] = 0
    for team in lineuplist:
        for pos in positions:
            player_cnt[team[pos]['Name']] = player_cnt[team[pos]['Name']] + 1
    return player_cnt
        
def display_lineups(lineup):
    y = lineup
    print '\n'
    print "Team Salary: ", y['TeamSalary'], " Team AVG Rank: ", y['Overallrank'], "  Team PPG: ", y['Teamppg'], " Team PPO: ", y['Teamppg'] / y['Oppscore'], " Opty score: ", y['Oppscore']
    positions = ['qb','rb1','rb2','wr1','wr2','wr3','te','flex','dst']

    table =[]
    for pos in positions:
        if pos != 'dst':
            teamtable = []
            headermap = [('Name','Name'),('teamAbbrev','Team'),('Salary','Salary'),('AvgPointsPerGame','PPG'),('Oppscore','TAR(weighted)'),('PtsPerOpp','PPO'),('Overallrank','Rank(pos)')]
            headertbl = []
            for z in headermap:
                teamtable.append(y[pos][z[0]])
                headertbl.append(z[1])
            table.append(teamtable)


    print tabulate(table, headers = headertbl)
    print y['dst']['Name'],y['dst']['Salary'], y['dst']['AvgPointsPerGame']
    print "\n"

def WriteListToCSV(csv_file,csv_columns,data_list):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
    return              

def get_bstlineqb(lineups):
    qbs = test.qbs()
    rbs = test.get_rankedlist(test.rb1s())
    print rbs
    wrs = test.get_rankedlist(test.wr1s())
    print wrs
    new_lineups = []
    for x in qbs:
        h = 0
        for lineup in lineups:
           if lineup['qb']['Name'] == x:
               if lineup['rb1']['Name'] == rbs[h]:
                   if lineup['wr1']['Name'] == wrs[h]:
                       if teamcheck(lineup):
                           lst.append(lineup)
               if lst:
                   best.append(sorted(lst, key = lambda k: k['Oppscore'], reverse=True)[0])
                h = h + 1
        for z in best:
            new_lineups.append(z)
    return new_lineups

def get_beststacked(lineups,num):
    qbs = test.qbs()    
    stacked = get_stacked(lineups,qbs)
    beststacked = []
    for q in qbs:
        besteams = []
        for team in stacked:
            if team['qb']['Name'] == q:
                if teamcheck(team):
                    besteams.append(team)
        z = 0
        if besteams:
            for x in besteams:
          
                while z < num:
                    beststacked.append(sorted(besteams, key = lambda k: k['Oppscore'],reverse=True)[z])
                    z = z + 1
    return beststacked
            

#best = get_stacked(teams,qb)
#cnt = 0
#new_teams = []
#for q in test.qbs():
#    for y in test.get_rbcomborank(test.get_rbcombos, test.rb1s, test.rb2s):
#        bestrbteams = []
#        for x in best:
#            if x['rb1']['Name'] == y[0] and x['rb2']['Name'] == y[1]: 
#                if teamcheck(x):
#                    bestrbteams.append(x)
#        z = 0
#        while z < 1:
#            new_teams.append(sorted(bestrbteams, key = lambda k: k['Oppscore'],reverse=True)[z])
#            z = z + 1
b = get_bstlineqb(teams)
for y in b:
    display_lineups(y)
print distribution(b,allplayers)


#csv_columns = ['QB','RB1','RB2','WR1','WR2','WR3','TE','FLEX','DST']
#csv_data_list = new_teams 
#
#currentPath = os.getcwd()
#csv_file = "/home/scrabbleadmin/nflproj/teams.csv"
#
#
#WriteListToCSV(csv_file,csv_columns,csv_data_list)
        

    

#print len(get_beststacked(get_stacked(teams,qb),qb,rb,wr,te))
#print len(get_stacked(teams,qb))
#bcnt = 0
#plyercount = {}
#allplayers = qb + rb + wr + te
#for p in allplayers:
#    plyercount[p] = 0
#for x in get_beststacked(get_stacked(teams,qb),qb,rb,wr,te):
#    display_lineups(x)
#    bcnt = bcnt +1
#    positions = ['qb','rb1','rb2','wr1','wr2','wr3','te','flex']
#    for pos in positions:
#        z = x[pos]['Name'] 
#        plyercount[z] = plyercount[z] + 1
#    
                

    



