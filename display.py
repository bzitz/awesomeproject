import json, team, nfldb
from sys import argv
from tabulate import tabulate

class Display(object):
    def __init__(self,jsonfile, displaytype):
        self.jsonfile = jsonfile
        self.displaytype = displaytype
        self.teams = {}
        
    def control(self):
        if self.displaytype == 'log':
            self.read_logfile("/home/scrabbleadmin/nflproj/teamlogs/"+self.jsonfile)

    def read_logfile(self, jsonlog):
        jsonfile = open(jsonlog, "r")
        self.teams = json.load(jsonfile)
        new_dict = {}
        print '\n'
        for x in self.teams:
            for y in self.teams[x]:
                newteam = team.Team()
                positions = newteam.return_pos()
                table = []
                for pos in positions:
                    if pos == 'dst':
                        oppscore = 0
                        efficiency = 0
                    else: 
                        oppscore = self.teams[x][y][pos]['Oppscore']
                        efficiency = float("{0:.2f}".format(float(self.teams[x][y][pos]['AvgPointsPerGame'])/float(oppscore) ))

                    table.append([
                        self.teams[x][y][pos]['Name'],
                        self.teams[x][y][pos]['teamAbbrev'],
                        self.teams[x][y][pos]['AvgPointsPerGame'],
                        self.teams[x][y][pos]['Value'],
                        oppscore,
                        efficiency,
                    ])
                print "Team Salary: ", self.teams[x][y]['TeamSalary'], "   Team PPG: ", self.teams[x][y]['Teamppg'] ,"  Team Targets: ", self.teams[x][y]['Oppscore'] 

                print tabulate(table, headers = ["Name","Team","PPG","$/Point","Opp Score", "PT/OPP"])
                print "\n"
                print "\n"

#    def print_topplayers(self, pos, stat, number):
#        newplayers = team.Player()
#        newplayers.import_json()
#        stats = []
#        playerlst = []
#        if pos!='DST':
#            for x in newplayers.players:
#                if newplayers.players

    
def display_log(logfile): 
    newdisplay = Display(logfile,"log")

    newdisplay.control()

def main(_, logfile):
    display_log(logfile)

if __name__=='__main__':
    main(*argv)
        
