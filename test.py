import team, decimal, nfldb, os, json, heapq, time
from operator import itemgetter
from tabulate import tabulate

def get_teams():
    newteam = team.Team()
    newteam.main()
    return newteam.team

x = 1
teamselected = []
while x < 100000:
    print x
    z = get_teams()
    if z['TeamSalary'] <= 50000 and z['Teamppg'] > 175 and z['Oppscore'] > 150:
        print 'great'
        print z['TeamSalary']
        teamselected.append(z)
    else:
        print 'no'
    x = x +1
    if len(teamselected) > 20:
        teamselected = sorted(teamselected, key=itemgetter('PPO'), reverse=True)
        teamselected.pop() 
print teamselected[0]['TeamSalary']   
print len(teamselected)

for y in teamselected:
    
    print '\n'
    print "Team Salary: ", y['TeamSalary'], " Team AVG Rank: ", y['Overallrank'], "  Team PPG: ", y['Teamppg'], " Team PPO: ", y['Teamppg'] / y['Oppscore'], " Opty score: ", y['Oppscore']
    newteam = team.Team()
    positions = newteam.return_pos()
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

    
