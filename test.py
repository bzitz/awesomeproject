import team, decimal, nfldb, os, json, heapq, time, itertools, random
import sqlite3 as lite
from operator import itemgetter
from tabulate import tabulate

p = team.Player('pos')
p.import_json()
player = p.players

def qbs():
    qb = [
        'Matthew Stafford', 
        'Andy Dalton',
        'Matt Ryan',
        'Philip Rivers',
        'Ryan Fitzpatrick',
        'Brian Hoyer'
        ]
    return qb

def rb1s():
    rb1 = [
        "Le'Veon Bell", 
        'Devonta Freeman',
        'Todd Gurley',
        'Charcandrick West',
        'Doug Martin',
        'Danny Woodhead',
        'Chris Johnson',
        'Antonio Andrews'
        ]
    return rb1

def rb2s():
    rb2 = [
        ]
    return rb2

def wr1s():
    wr1 = [
        'Julio Jones', 
        'Keenan Allen',
        'Stefon Diggs',
        'DeAndre Hopkins',
        'Calvin Johnson',
        'Jeremy Maclin',
        'Antonio Brown',
        'Martavis Bryant',
        'Alshon Jeffery',
        'Mike Evans',
        'Kendall Wright',
        'Marvin Jones',
        'Brandon Marshall',
        'Ted Ginn Jr.'
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
        'Tyler Eifert',
        'Ladarius Green',
        'Jacob Tamme',
        'Eric Ebron',
        'Benjamin Watson',
        ]
    return te

def dsts():    
    dst = [
        'Cardinals ', 
        'Falcons ', 
        'Rams ',
        'Seahawks ',
        'Panthers ',
        ]
    return dst

def flex():
    flx = wr1s() + tes() + rb1s()
    return flx

def get_flex(salary,r1,r2,w1,w2,w3,te):
    choices = flex()
    chosen = [r1,r2,w1,w2,w3,te]
    posflex = []
    for x in choices:
        if x not in chosen:
            if int(player[x]['Salary']) <= (50000 - int(salary)):
                posflex.append((x,player[x]['Salary']))
    return sorted(posflex, key=lambda y: y[1],reverse=True)[0][0]

def get_dst():
    dfense = dsts()
    std = random.choice(dfense)
    return std
    
def get_rankedlist(listname):
    ranked = []
    rankedlist = []
    for name in listname:
        ranked.append((name,player[name]['Oppscore']))
    for x in sorted(ranked, key = lambda k: k[1], reverse=True):
        rankedlist.append(x[0])
    return rankedlist

def get_rbcombos(rb1):
    r1 = rb1()
    rbcombo = []
    for combo in itertools.combinations(r1,2):
        rbcombo.append(combo)
    return rbcombo
def get_rbcomborank(rbcombos, rb1):
    combos = rbcombos(rb1)
    ranked = []
    nameonly = []
    for combo in combos:
        total = player[combo[0]]['Oppscore'] + player[combo[1]]['Oppscore']
        ranked.append((combo[0],combo[1],total))
    for x in sorted(ranked, key = lambda k: k[2], reverse=True):
        nameonly.append((x[0], x[1], x[2]))
    return nameonly
        
def get_wrcombos(wr1):
    w1 = wr1()
    wrcombo = []
    for combo in itertools.combinations(w1,3):
        wrcombo.append(combo)
    return wrcombo
def get_wrcomborank(wrcombos,wr1):
    combos = wrcombos(wr1)
    ranked = []
    nameonly = []
    for combo in combos:
        total = player[combo[0]]['Oppscore'] + player[combo[1]]['Oppscore'] + player[combo[2]]['Oppscore']
        ranked.append((combo[0],combo[1], combo[2], total))
    for x in sorted(ranked, key = lambda k: k[3], reverse=True):
        nameonly.append((x[0], x[1], x[2]))
    return nameonly

def check_team(team):
    if team['TeamSalary'] <= 50000:
        if team['rb1']['teamAbbrev'] != team['wr1']['teamAbbrev'] and team['rb1']['teamAbbrev'] != team['wr2']['teamAbbrev'] and team['rb1']['teamAbbrev'] != team['wr3']['teamAbbrev'] and team['rb1']['teamAbbrev'] != team['te']['teamAbbrev'] and team['rb1']['teamAbbrev'] != team['flex']['teamAbbrev']:
            if team['rb2']['teamAbbrev'] != team['wr1']['teamAbbrev'] and team['rb2']['teamAbbrev'] != team['wr2']['teamAbbrev'] and team['rb2']['teamAbbrev'] != team['wr3']['teamAbbrev'] and team['rb2']['teamAbbrev'] != team['te']['teamAbbrev'] and team['rb2']['teamAbbrev'] != team['flex']['teamAbbrev']:
                if team['qb']['teamAbbrev'] != team['rb1']['teamAbbrev'] and team['qb']['teamAbbrev'] != team['rb2']['teamAbbrev']:
                    if team['wr1']['teamAbbrev'] != team['flex']['teamAbbrev'] and team['wr2']['teamAbbrev'] != team['flex']['teamAbbrev'] and team['wr3']['teamAbbrev'] != team['flex']['teamAbbrev']:
                        if team['wr1']['teamAbbrev'] != team['te']['teamAbbrev'] and team['wr2']['teamAbbrev'] != team['te']['teamAbbrev'] and team['wr3']['teamAbbrev'] != team['te']['teamAbbrev']:
                            return True

def connect(command,stats):
    con = lite.connect('dksalary.db')

    with con:
        cur = con.cursor()
        cur.execute(command,stats)
def update_teams(team):
    total = 0
    x = team
    connect("INSERT INTO teams (qb,rb1,rb2,wr1,wr2,wr3,te,flex,dst,oppscore,teamsalary,ppo,teamppg) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(x['qb']['Name'],x['rb1']['Name'],x['rb2']['Name'],x['wr1']['Name'],x['wr2']['Name'],x['wr3']['Name'],x['te']['Name'],x['flex']['Name'], x['dst']['Name'],x['Oppscore'],x['TeamSalary'],x['PPO'],x['Teamppg']))


#print len(get_rbcomborank(get_rbcombos, rb1s))
#print len(get_wrcomborank(get_wrcombos, wr1s))
##print get_wrcombos(wr1s,wr2s)
#count = 0
#allpos = [qbs(),get_rbcombos(rb1s),get_wrcombos(wr1s),tes()]
#print allpos
#lineup = []
#
#for x in itertools.product(*allpos):
#    salary = 0
#    qb = x[0]
#    rb1 = x[1][0]
#    rb2 = x[1][1]
#    wr1 = x[2][0]
#    wr2 = x[2][1]
#    wr3 = x[2][2]
#    te = x[3]
#    d = get_dst()
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
#        flx = get_flex(salary,rb1,rb2,wr1,wr2,wr3,te)
#        t.append(('FLEX',flx,player[flx]['Salary']))
#        new_team = team.Team(qb,rb1,rb2,wr1,wr2,wr3,te,flx,d)
#        new_team.main()
#        if check_team(new_team.team):
#            if new_team.team not in lineup:
#                update_teams(new_team.team)
#                count = count + 1
#                print count
#                print new_team.qb
#        else:
#            print 'no'

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
