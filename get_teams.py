import team, decimal, nfldb, os, json, heapq, time
from tabulate import tabulate

def generate_teams(t):
    teams = {}

    itter = 1
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
        sortedteams[x]= (teams[x]['Oppscore'] )
    top10 = heapq.nlargest(40,sortedteams, key=sortedteams.get)
    newteams = {}
    for x in top10:
        newteams[x] = teams[x]
        print '\n'
        print "Team Salary: ", teams[x]['TeamSalary'], " Team AVG Rank: ", teams[x]['Overallrank'], "  Team PPG: ", teams[x]['Teamppg'], " Team PPO: ", teams[x]['Teamppg'] / teams[x]['Oppscore'], " Opty score: ", teams[x]['Oppscore']
        positions = newteam.return_pos()
        table =[]
        for pos in positions:
            if pos != 'dst':
                teamtable = []    
                headermap = [('Name','Name'),('Salary','Salary'),('AvgPointsPerGame','PPG'),('Oppscore','TAR(weighted)'),('Overallrank','Rank(pos)')]
                headertbl = []
                for z in headermap:
                    teamtable.append(teams[x][pos][z[0]])
                    headertbl.append(z[1])
                table.append(teamtable)                

            
        print tabulate(table, headers = headertbl)
        print teams[x]['dst']['Name'],teams[x]['dst']['Salary'], teams[x]['dst']['AvgPointsPerGame']
        print headertbl
    print "\n"

    return newteams
x = 0
teamlog = {}
while x < 1:
    teamlog[x] = generate_teams(x)
    print x
    x = x + 1
epoch_time = str(time.time())
json_file = open('/home/scrabbleadmin/nflproj/teamlogs/'+ epoch_time + '.json', 'w')
json_file.write(json.dumps(teamlog,indent=2))
json_file.close
