import team, decimal, nfldb, os, json, heapq, time, itertools, random
from operator import itemgetter
from tabulate import tabulate

p = team.Player('pos')
p.import_json()
player = p.players

def qbs():
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
    return qb

def rb1s():
    rb1 = [
        "Le'Veon Bell", 
        "Le'Veon Bell", 
        'Jamaal Charles',
        'Latavius Murray',
        'Devonta Freeman',
        'Jamaal Charles',
        'Matt Forte',
        'Latavius Murray',
        'Devonta Freeman',
        'Jamaal Charles',
        'Matt Forte',
        'Latavius Murray',
        ]
    return rb1

def rb2s():
    rb2 = [
        'Justin Forsett', 
        'Justin Forsett', 
        'Justin Forsett', 
        'Justin Forsett', 
        'Dion Lewis', 
        'Dion Lewis', 
        'Dion Lewis', 
        'LeGarrette Blount',
        'LeGarrette Blount',
        'Karlos Williams',
        'Karlos Williams',
        'Todd Gurley',
        'Todd Gurley',
        'Todd Gurley',
        'Doug Martin',
        'C.J. Anderson',
        'C.J. Anderson',
        'Karlos Williams',
        'Todd Gurley',
        'Doug Martin',
        'C.J. Anderson'
        ]
    return rb2

def wr1s():
    wr1 = [
        'Julio Jones', 
        'Julio Jones', 
        'Odell Beckham', 
        'Odell Beckham', 
        'Larry Fitzgerald', 
        'Larry Fitzgerald', 
        'Keenan Allen',
        'Keenan Allen',
        'Julian Edelman',
        'Demaryius Thomas',
        'Demaryius Thomas'
        ]
    return wr1

def wr2s():
    wr2 = [
        'Jeremy Maclin', 
        'Allen Hurns', 
        'Allen Hurns', 
        'Amari Cooper', 
        'Amari Cooper', 
        'Michael Crabtree', 
        'Kendall Wright',
        'Kendall Wright'
        ] 
    return wr2

def wr3s():
    wr3 = [
        'Leonard Hankerson',
        'Pierre Garcon', 
        'Terrance Williams', 
        'Leonard Hankerson',
        'Pierre Garcon', 
        'Terrance Williams', 
        'Doug Baldwin',
        'Doug Baldwin',
        'Martavis Bryant',
        'Eddie Royal',
        'Eddie Royal'
        ]
    return wr3

def tes():
    te = [
        'Rob Gronkowski', 
        'Travis Kelce',
        'Antonio Gates',
        'Owen Daniels', 
        'Martellus Bennett'
        ]
    return te

def dsts():    
    dst = [
        'Bengals ', 
        'Cardinals ', 
        'Chiefs ', 
        'Giants ', 
        'Bears ', 
        'Jaguars '
        ]
    return dst

def flex():
    flx = wr1s() + wr2s() + wr3s() + te()
    return flx

def get_flex(salary,r1,r2,w1,w2,w3,te,choices):
    chosen = [r1,r2,w1,w2,w3,te]
    posflex = []
    for x in choices:
        if x not in chosen:
            if int(player[x]['Salary']) <= (50000 - int(salary)):
                posflex.append((x,player[x]['Salary']))
    return sorted(posflex, key=lambda y: y[1],reverse=True)[0][0]

def get_dst(defense):
    std = random.choice(defense)
    return std
    
def get_rankedlist(listname):
    ranked = []
    rankedlist = []
    for name in listname:
        ranked.append((name,player[name]['Oppscore']))
    for x in sorted(ranked, key = lambda k: k[1], reverse=True):
        rankedlist.append(x[0])
    return rankedlist

def get_rbcombos(rb1,rb2):
    r1 = rb1()
    r2 = rb2()
    rbs = [r1,r2]
    rbcombo = []
    for combo in itertools.product(*rbs):
        rbcombo.append(combo)
    return rbcombo
def get_rbcomborank(rbcombos, rb1, rb2):
    combos = rbcombos(rb1, rb2)
    ranked = []
    nameonly = []
    for combo in combos:
        total = player[combo[0]]['Oppscore'] + player[combo[1]]['Oppscore']
        ranked.append((combo[0],combo[1],total))
    for x in sorted(ranked, key = lambda k: k[2], reverse=True):
        nameonly.append((x[0], x[1], x[2]))
    return nameonly
        

def get_wrcombos(wr1, wr2, wr3):
    w1 = wr1()
    w2 = wr2()
    w3 = wr3()
    wrs = [w1, w2, w3]
    wrcombo = []
    for combo in itertools.product(*wrs):
        wrcombo.append(combo)
    return wrcombo
def get_wrcomborank(wrcombos,wr1,wr2,wr3):
    combos = wrcombos(wr1,wr2,wr3)
    ranked = []
    nameonly = []
    for combo in combos:
        total = player[combo[0]]['Oppscore'] + player[combo[1]]['Oppscore'] + player[combo[2]]['Oppscore']
        ranked.append((combo[0],combo[1], combo[2], total))
    for x in sorted(ranked, key = lambda k: k[3], reverse=True):
        nameonly.append((x[0], x[1], x[2]))
    return nameonly



#print len(get_rbcomborank(get_rbcombos, rb1s, rb2s))
#print len(get_wrcomborank(get_wrcombos, wr1s, wr2s, wr3s))
#print get_wrcombos(wr1s,wr2s)
#allpos = [qb,rbcombo,wrcombo,te]
#lineup = []
#for x in itertools.product(*allpos):
#    salary = 0
#    qb = x[0]
#    rb1 = x[1][0]
#    rb2 = x[1][1]
#    wr1 = x[2][0]
#    wr2 = x[2][1]
#    wr3 = x[2][2]
#    te = x[3]
#    d = get_dst(dsts)
#    t = [
#            ('QB',qb,player[qb]['Salary']),
#            ("RB1",rb1,player[rb1]['Salary']),
#            ("RB2",rb2,player[rb2]['Salary']),
#            ("WR1",wr1,player[wr1]['Salary']),
#            ("WR2",wr2,player[wr2]['Salary']),
#            ("WR3",wr3,player[wr3]['Salary']),
#            ("TE",te,player[te]['Salary']),
#            ("DST",d,player[d]['Salary'])
#            ]
#    for y in t:
#        salary = salary + int(y[2])
#    if salary > 38000 and salary < 45600:
#        flx = get_flex(salary,rb1,rb2,wr1,wr2,wr3,te,flex)
#        t.append(('FLEX',flx,player[flx]['Salary']))
#        new_team = team.Team(qb,rb1,rb2,wr1,wr2,wr3,te,flx,d)
#        new_team.main()
#        if new_team.teamopp > 190:
#            if new_team.team not in lineup:
#                lineup.append(new_team.team)
#                count = count + 1
#                print count
#                print qb
#
cntr = 0
if True == False:
    for y in lineup:
        
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

#json_file = open('/home/scrabbleadmin/nflproj/teamlogs/topteams.json', 'w')
#json_file.write(json.dumps(lineup,indent=2))
#print rbcnt
#print len(rbcombo)
#print wrcnt
#print len(wrcombo)
