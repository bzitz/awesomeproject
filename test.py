import team, decimal, nfldb, os, json, heapq, time, itertools, random
from operator import itemgetter
from tabulate import tabulate

qb = [
    'Philip Rivers',
    'Carson Palmer', 
    'Blake Bortles', 
    'Tom Brady', 
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
    ]
wr1 = [
    'Julio Jones', 
    'Odell Beckham', 
    'Larry Fitzgerald', 
    'Keenan Allen',
    'Julian Edelman'
    ]
wr2 = [
    'Jeremy Maclin', 
    'Allen Hurns', 
    'Leonard Hankerson'] 
wr3 = [
    'Pierre Garcon', 
    'Amari Cooper', 
    'Michael Crabtree', 
    'Terrance Williams', 
    'Doug Baldwin'
    ]
te = ['Rob Gronkowski', 'Jordan Reed', 'Travis Kelce','Ladarius Green', 'Martellus Bennett']
dsts = ['Bengals ', 'Cardinals ', 'Chiefs ', 'Giants ', 'Bears ', 'Jaguars ']
flex = wr1 + wr2 + wr3 + te
rbs = [rb1,rb2]
wrs = [wr1,wr2,wr3]

rbcombo = []
rbcnt = 0
wrcombo = []
wrcnt = 0
count = 0
lineup = [] 

p = team.Player('pos')
p.import_json()
player = p.players

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
    

for combo in itertools.product(*rbs):
    rbcombo.append(combo)
    rbcnt = rbcnt + 1
for combo in itertools.product(*wrs):
    wrcombo.append(combo)
    wrcnt = wrcnt + 1


allpos = [qb,rbcombo,wrcombo,te]
lineup = []
for x in itertools.product(*allpos):
    salary = 0
    qb = x[0]
    rb1 = x[1][0]
    rb2 = x[1][1]
    wr1 = x[2][0]
    wr2 = x[2][1]
    wr3 = x[2][2]
    te = x[3]
    d = get_dst(dsts)
    t = [
            ('QB',qb,player[qb]['Salary']),
            ("RB1",rb1,player[rb1]['Salary']),
            ("RB1",rb2,player[rb2]['Salary']),
            ("WR1",wr1,player[wr1]['Salary']),
            ("WR2",wr2,player[wr2]['Salary']),
            ("WR3",wr3,player[wr3]['Salary']),
            ("TE",te,player[te]['Salary']),
            ("DST",d,player[d]['Salary'])
            ]
    for y in t:
        salary = salary + int(y[2])
    if salary > 38000 and salary < 45600:
        flx = get_flex(salary,rb1,rb2,wr1,wr2,wr3,te,flex)
        t.append(('FLEX',flx,player[flx]['Salary']))
        new_team = team.Team(qb,rb1,rb2,wr1,wr2,wr3,te,flx,d)
        new_team.main()
        if new_team.teamopp > 200:
            if new_team.team not in lineup:
                lineup.append(new_team.team)
                count = count + 1
                print count
                print qb

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

json_file = open('/home/scrabbleadmin/nflproj/teamlogs/topteams.json', 'w')
json_file.write(json.dumps(lineup,indent=2))
print rbcnt
print len(rbcombo)
print wrcnt
print len(wrcombo)
