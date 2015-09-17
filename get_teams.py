import team, decimal, nfldb, os, json, heapq 
from tabulate import tabulate

def generate_teams(t):
    teams = {}

    itter = 500000
    x = 0
    while x < itter:
        newteam = team.Team()
        newteam.main()
    #    os.system('clear')
        print x, "out of", itter, t 
        if newteam.teamsalary <= newteam.team_maxsalary:
            teams[x] = newteam.team
        x = x + 1
    sortedteams = {}
    for x in teams:
        sortedteams[x]= (teams[x]['Oppscore'])
    top10 = heapq.nlargest(10,sortedteams, key=sortedteams.get)
    newteams = {}
    for x in top10:
        newteams[x] = teams[x]
        print '\n'
        print "Team Salary: ", teams[x]['TeamSalary'], " Team OPP: ", teams[x]['Oppscore']
        positions = newteam.return_pos()
        table =[]
        for pos in positions:
            if pos == 'dst':
                oppscore = 0
            else:
                oppscore = teams[x][pos]['Oppscore']
            table.append([
                teams[x][pos]['Name'],
                teams[x][pos]['teamAbbrev'], 
                teams[x][pos]['Salary'],
                teams[x][pos]['AvgPointsPerGame'], 
                teams[x][pos]['Value'], 
                oppscore
            ])
                
        print tabulate(table, headers = ["Name","Team","Salary","PPG","$/Point","OppScore"])
    print "\n"

    return newteams
x = 0
teamlog = {}
while x < 1:
    teamlog[x] = generate_teams(x)
    print x
    x = x + 1

json_file = open('teamlog.json', 'w')
json_file.write(json.dumps(teamlog,indent=2))
json_file.close
