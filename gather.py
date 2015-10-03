import csv, json
from tabulate import tabulate


jsonfile = open('teamlogs/topteams.json', 'r')
teams = json.load(jsonfile)
gathered = []
totalopp = 0

qb = [
    'Derek Carr',
    'Aaron Rodgers',
    'Blake Bortles',
    'Andy Dalton',
    'Matt Ryan',
    'Colin Kaepernick'
    ]
rb = [
    'Adrian Peterson',
    'Jamaal Charles',
    'Latavius Murray',
    'Mark Ingram',
    'Joseph Randle',
    'Devonta Freeman',
    'Carlos Hyde',
    'Alfred Blue',
    'Karlos Williams']
wr = [
    'Julio Jones',
    'Odell Beckham',
    'Demaryius Thomas',
    'A.J. Green',
    'Calvin Johnson',
    'Randall Cobb',
    'DeAndre Hopkins',
    'Keenan Allen',
    'Larry Fitzgerald',
    'Amari Cooper',
    'Michael Crabtree',
    'Allen Robinson',
    'James Jones',
    ]
te = ['Jason Witten', 'Jordan Reed', 'Tyler Eifert', 'Greg Olsen', 'Jimmy Graham', 'Martellus Bennett']

def get_stacked(teamlst,qblst):
    stacked = []
    for x in teamlst:
        for z in qblst:
            if x['qb']['Name'] == z:
                if x['wr1']['teamAbbrev'] == x['qb']['teamAbbrev'] or x['wr2']['teamAbbrev'] == x['qb']['teamAbbrev'] or x['wr3']['teamAbbrev'] == x['qb']['teamAbbrev']:
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
            if t['Oppscore'] > 206:
                best_lineups.append(t)
        if rbqbcheck(t) and excluderb(t,"Devonta Freeman") and excluderb(t,"Jamaal Charles")and excludewr(t,"Larry Fitzgerald") and wrwrcheck(t):
            if t['Oppscore'] > 206:
                best_lineups.append(t)
        if rbqbcheck(t) and excluderb(t,"Devonta Freeman") and excludewr(t,"Larry Fitzgerald") and excludewr(t,"Michael Crabtree") and wrwrcheck(t):
            if t['Oppscore'] > 204:
                best_lineups.append(t)
        if rbqbcheck(t) and excluderb(t,"Devonta Freeman") and excludewr(t,"Larry Fitzgerald") and excludewr(t,"Michael Crabtree") and wrwrcheck(t):
            if t['Oppscore'] > 210:
                best_lineups.append(t)
            
    return best_lineups

def rbqbcheck(lineup):
    if lineup['qb']['teamAbbrev'] != (lineup['rb1']['teamAbbrev'] or lineup['rb2']['teamAbbrev']):
        if (lineup['rb1']['teamAbbrev'] or lineup['rb2']['teamAbbrev']) != (lineup['wr1']['teamAbbrev'] or lineup['wr2']['teamAbbrev'] or lineup['wr3']['teamAbbrev']):
            return True

def wrwrcheck(lineup):
    if lineup['wr1']['teamAbbrev'] != (lineup['wr2']['teamAbbrev'] or lineup['wr3']['teamAbbrev']):
        if lineup['wr2']['teamAbbrev'] != (lineup['wr1']['teamAbbrev'] or lineup['wr3']['teamAbbrev']):
            if lineup['wr3']['teamAbbrev'] != (lineup['wr1']['teamAbbrev'] or lineup['wr2']['teamAbbrev']):
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


stck = get_stacked(teams,qb)
for t in stck:
    

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
#print bcnt
#print plyercount 
                

    



