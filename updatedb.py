import sqlite3 as lite
import json

jsonfile = open('teamlogs/topteams.json', 'r')
teams = json.load(jsonfile)

def connect(command,stats):
    con = lite.connect('dksalary.db')

    with con:
        cur = con.cursor()
        cur.execute(command,stats)

def update_teams():
    total = 0
    for x in sorted(teams, key=lambda x: x['Oppscore'], reverse = True):
        connect("INSERT INTO teams (qb,rb1,rb2,wr1,wr2,wr3,te,flex,dst,oppscore,teamsalary,ppo,teamppg) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(x['qb']['Name'],x['rb1']['Name'],x['rb2']['Name'],x['wr1']['Name'],x['wr2']['Name'],x['wr3']['Name'],x['te']['Name'],x['flex']['Name'], x['dst']['Name'],x['Oppscore'],x['TeamSalary'],x['PPO'],x['Teamppg']))

        total = total + 1
        print total 

update_teams()
                



    
