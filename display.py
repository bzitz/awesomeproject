import json, team, nfldb
from tabulate import tabulate

class Display(object):
    def __init__(self,jsonfile, displaytype):
        self.jsonfile = jsonfile
        self.displaytype = displaytype
        self.teams = {}
    def control(self):
        if self.displaytype == 'log':
            self.read_logfile(self.jsonfile)

    def read_logfile(self, jsonlog):
        jsonfile = open(jsonlog, "r")
        self.teams = json.load(jsonfile)
        new_dict = {}
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        print '\n'
        for x in self.teams:
            for y in self.teams[x]:
                newteam = team.Team()
                positions = newteam.return_pos()
                table = []
                for pos in positions:
                    table.append([
                        self.teams[x][y][pos]['Name'],
                        self.teams[x][y][pos]['teamAbbrev'],
                        self.teams[x][y][pos]['AvgPointsPerGame'],
                        self.teams[x][y][pos]['Value'],
                        self.teams[x][y][pos]['tchpergame'],
                        self.teams[x][y][pos]['targin20'],
                        self.teams[x][y][pos]['percentin20'],
                        self.teams[x][y][pos]['targin10'],
                        self.teams[x][y][pos]['percentin10'],
                    ])
                print "Team Salary: ", self.teams[x][y]['TeamSalary'], "   Team PPG: ", self.teams[x][y]['Teamppg'] ,"  Team Targets: ", self.teams[x][y]['Targets'], "  Targin20", self.teams[x][y]['TeamTch20'], "  Targin10", self.teams[x][y]['TeamTch10']

                print tabulate(table, headers = ["Name","Team","PPG","$/Point","Touches/game(2015)","Tinside20","%%Team","Tinside10","%%Team"])
                print "\n"
                print "\n"

newdisplay = Display("teamlog.json","log")

newdisplay.control()
    
        
