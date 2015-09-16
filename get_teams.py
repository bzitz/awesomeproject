import team, decimal, nfldb, os 
from tabulate import tabulate

teams = {}
team_avg_score = [0,0,0,0,0]
itter = 2
x = 0
while x < itter:
    newteam = team.Team()
    newteam.main()
    os.system('clear')
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
                if srtlist[4] > 0:
                    del teams[srtlist[4]]
                value = srtlist[4]
                #print "removing" , srtlist[4]
                srtlist.pop(4)
                #print "I removed on %d try" % y
                #print srtlist
                #print "adding " , newteam.teamavg
                srtlist.append(round(a,3))
                #print "I added on %d try" % y
                #print srtlist
                    
                y = 5
            team_avg_score = srtlist
            y = y + 1
    x = x + 1

def target_pergame(player):
    db = nfldb.connect()
    q = nfldb.Query(db)
    opp20 = nfldb.FieldPosition.from_str('OPP 20')
    q.game(season_year=2014, season_type='Regular')
    #q.play(yardline__ge=opp20)
    q.player(full_name=player)
    #q.player(team__ne='UNK')
    total = 0
    for game in q.as_aggregate():
        total = total + game.rushing_att + game.receiving_tar
        #print game.player, (game.rushing_att + game.receiving_tar)/16
    return total/16


for x in teams:
    print '\n'
    print "Team Salary: ", teams[x]['TeamSalary'], " Team PPG: ", x ,"Team Targets: ", teams[x]['Targets']
    positions = newteam.return_pos()
    table =[]
    for pos in positions:
        table.append([teams[x][pos]['Name'],teams[x][pos]['teamAbbrev'], teams[x][pos]['AvgPointsPerGame'], teams[x][pos]['Value'], target_pergame(teams[x][pos]['Name'])])
    print tabulate(table, headers = ["Name","Team","PPG","$/Point","Touches/game"])
    print x
print "\n"
print sum(team_avg_score)/5


