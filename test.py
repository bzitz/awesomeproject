import team, decimal, nfldb, os, json, heapq, time
from operator import itemgetter
from tabulate import tabulate


def pick_team():
    t = team.Player('pos')
    t.get_pos()
    count = 0
    total = 0
    best_teams = []
    while count < 100:
        for qb in t.qbs:
            for rb1 in t.rb1s:
                for rb2 in t.rb2s:
                    for wr1 in t.wr1s:
                        for wr2 in t.wr2s:
                            for wr3 in t.wr3s:
                                for te in t.tes:
                                    for flex in t.pick_flex(wr1,wr2,wr3,te):
                                            newteam = team.Team(qb,rb1,rb2,wr1,wr2,wr3,te,flex)
                                            newteam.main()
                                            #print newteam.team['TeamSalary']
                                            total = total + 1
                                            if newteam.team['TeamSalary'] <= 50000 and newteam.team['Oppscore'] > 220:
                                                if newteam.team not in best_teams:
                                                    best_teams.append(newteam.team)
                                                    count = count + 1
                                            print count, total
    return best_teams
                                   

for y in pick_team():
    
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

    
