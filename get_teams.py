import team, decimal, nfldb, os, json 
from tabulate import tabulate

def generate_teams():
    teams = {}
    team_avg_score = [0,0,0,0,0,0,0,0,0,0]
    itter = 500000
    x = 0
    while x < itter:
        newteam = team.Team()
        newteam.main()
    #    os.system('clear')
        print x, "out of", itter 
        if newteam.teamsalary <= newteam.team_maxsalary:
            y = 0
            while y < len(team_avg_score):
                srtlist = sorted(team_avg_score, reverse=True)
                if newteam.teamavg > srtlist[y]:
                    a = decimal.Decimal(str(newteam.teamavg))
                    b = decimal.Decimal(str(newteam.teamsalary))
                   # print round(a,3)
                    teams[round(a,3)] = newteam.team
                    teams[round(a,3)]['TeamSalary'] = newteam.teamsalary
                    if srtlist[9] > 0:
                        del teams[srtlist[9]]
                    value = srtlist[9]
                    #print "removing" , srtlist[4]
                    srtlist.pop(9)
                    #print "I removed on %d try" % y
                    #print srtlist
                    #print "adding " , newteam.teamavg
                    srtlist.append(round(a,3))
                    #print "I added on %d try" % y
                    #print srtlist
                        
                    y = 10
                team_avg_score = srtlist
                y = y + 1
        x = x + 1

    for x in teams:
        print '\n'
        print "Team Salary: ", teams[x]['TeamSalary'], " Team PPG: ", x ,"Team Targets: ", teams[x]['Targets']
        positions = newteam.return_pos()
        table =[]
        for pos in positions:
            table.append([
                teams[x][pos]['Name'],
                teams[x][pos]['teamAbbrev'], 
                teams[x][pos]['AvgPointsPerGame'], 
                teams[x][pos]['Value'], 
                teams[x][pos]['tchpergame'], 
                teams[x][pos]['targin20'],
                teams[x][pos]['percentin20'],
                teams[x][pos]['targin10'],
                teams[x][pos]['percentin10'],
            ])
                
        print tabulate(table, headers = ["Name","Team","PPG","$/Point","Touches/game(2015)","Tinside20","%%Team","Tinside10","%%Team"])
    print "\n"
    print sum(team_avg_score)/10
    return teams
x = 0
teamlog = {}
while x < 10:
    teamlog[x] = generate_teams()
    x = x + 1

json_file = open('teamlog.json', 'w')
json_file.write(json.dumps(teamlog,indent=2))
json_file.close
