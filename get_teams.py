import team, decimal, nfldb, os, json, heapq 
from tabulate import tabulate

def generate_teams(t):
    teams = {}

    itter = 100000
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
        sortedteams[x]= ((teams[x]['Targets'] + int(teams[x]['Teamppg']) + (2 * teams[x]['TeamTch20']) + (4 * teams[x]['TeamTch10'])) / 4 )
    top5 = heapq.nlargest(10,sortedteams, key=sortedteams.get)
    newteams = {}
    for x in top5:
        newteams[x] = teams[x]
        print '\n'
        print "Team Salary: ", teams[x]['TeamSalary'], " Team PPG: ", teams[x]['Teamppg'] ,"Team Targets: ", teams[x]['Targets'], "Targin20", teams[x]['TeamTch20'], "Targin10", teams[x]['TeamTch10']
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

    return newteams
x = 0
teamlog = {}
while x < 6:
    teamlog[x] = generate_teams(x)
    print x
    x = x + 1

json_file = open('teamlog.json', 'w')
json_file.write(json.dumps(teamlog,indent=2))
json_file.close
