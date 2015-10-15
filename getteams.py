import sqlite3 as lite
import json,csv,test,operator,random

allplayers = test.qbs() + test.rb1s() + test.rb2s() + test.wr1s() + test.wr2s() + test.wr3s() + test.tes()

def connect(command,options):
    con = lite.connect('dksalary.db')

    with con:
        #con.row_factory = lite.row
        cur = con.cursor()

        cur.execute(command,options)
        rows = cur.fetchall()
    return rows

def WriteListToCSV(csv_file,csv_columns,data_list):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return 

def get_lineups():
    lineups = []
    while len(lineups) < 100:

        rb1 = random.choice(test.rb1s())
        print rb1
        rb2 = random.choice(test.rb2s())
        print rb2
        wr1 = random.choice(test.wr1s())
        print wr1
        wr2 = random.choice(test.wr2s())
        print wr2
        wr3 = random.choice(test.wr3s())
        print wr3
        te = random.choice(test.tes())
        print te
        for x in test.qbs():
            results = connect("SELECT qb,rb1,rb2,wr1,wr2,wr3,te,flex,dst,oppscore FROM teams WHERE qb=? and wr1=? and wr2=? and wr3=? and rb1=? and rb2=? and te=? ORDER BY oppscore DESC LIMIT 1", (x,wr1,wr2,wr3,rb1,rb2,te))
            if results:
                for row in results:
                    lineups.append(row)
        print len(lineups)

            


    return sorted(lineups, key=lambda k: k[9], reverse=True)

def distribute(lineuplist, players):
    roster = []
    player_cnt = {}
    for p in players:
        player_cnt[p] = 0
    for team in lineuplist:
        for player in team[:8]:
            player_cnt[player] = player_cnt[player] + 1
    return player_cnt

lines = get_lineups()[:100]

dist =  distribute(lines,allplayers)
new_lines = []
print "QUATERBACKS"
for x in test.qbs():
    print x,dist[x] 
print "RUNNING BACK 1"
for x in ["Le'Veon Bell", "Jamaal Charles", "Matt Forte", "Latavius Murray", "Devonta Freeman"]:
    print x,dist[x]
print "RUNNING BACK 2"
for x in ["Justin Forsett", "Dion Lewis", "LeGarrette Blount", "Karlos Williams", "Todd Gurley", "Doug Martin", "C.J. Anderson"]:
    print x, dist[x]
print "WIDE RECEIVER 1"
for x in ["Julio Jones", "Odell Beckham", "Larry Fitzgerald", "Keenan Allen", "Demaryius Thomas"]:
    print x, dist[x]
print "WIDE RECEIVER 2"
for x in ["Jeremy Maclin","Allen Hurns", "Amari Cooper","Michael Crabtree", "Kendall Wright"]:
    print x, dist[x]
print "WIDE RECEIVER 3"
for x in ['Leonard Hankerson',
        'Pierre Garcon',
        'Terrance Williams',
        'Doug Baldwin',
        'Martavis Bryant',
        'Eddie Royal'
        ]:
    print x, dist[x]

print "TIGHT ENDS"
for x in [
        'Rob Gronkowski',
        'Travis Kelce',
        'Antonio Gates',
        'Owen Daniels',
        'Martellus Bennett'
        ]:
    print x, dist[x]



print len(lines)
for x in lines:
    line = [x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8]]
    if line not in new_lines:
        new_lines.append(line)
        

csv_columns = ['QB','RB1','RB2','WR1','WR2','WR3','TE','FLEX','DST']
csv_data_list = new_lines

csv_file = "/home/scrabbleadmin/nflproj/week5teams.csv"


WriteListToCSV(csv_file,csv_columns,csv_data_list)

