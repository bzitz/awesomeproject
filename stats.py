import nfldb
class Stats(object):
    def __init__(self):
        self.seasontargets = {}
        self.in20targets = 0
        self.in10targets = 0
        self.teamin20targets = 0
        self.teamin10targets =0


    def playerstats(self, **kwargs):
        player = kwargs['player']
        db = nfldb.connect()
        q = nfldb.Query(db)
        q.game(season_year=kwargs['season'], season_type='Regular')
        if kwargs['targtype'] == "non-redzone":
            pos1 = nfldb.FieldPosition.from_str('OWN 1')
            pos2 = nfldb.FieldPosition.from_str('OPP 21')
        #OPP 20 to OPP 10 yardline
        elif kwargs['targtype'] == 'redzone':
            pos1 = nfldb.FieldPosition.from_str('OPP 20')
            pos2 = nfldb.FieldPosition.from_str('OPP 11')
        #OPP 10 to OPP 6
        elif kwargs['targtype'] == 'goaline1':
            pos1 = nfldb.FieldPosition.from_str('OPP 10')
            pos2 = nfldb.FieldPosition.from_str('OPP 6')
        # OPP 5 to OPP 3
        elif kwargs['targtype'] == 'goaline2':
            pos1 = nfldb.FieldPosition.from_str('OPP 5')
            pos2 = nfldb.FieldPosition.from_str('OPP 3')
        #OPP 2 or OPP 1
        elif kwargs['targtype'] == 'goaline3':
            pos1 = nfldb.FieldPosition.from_str('OPP 2')
            pos2 = nfldb.FieldPosition.from_str('OPP 1')
        
        q.play(yardline__ge=pos1)
        q.play(yardline__le=pos2)
        q.player(full_name= player)
        for pp in q.as_aggregate():
            return pp
    
    def carries(self,player,zone,season):
        car = self.playerstats(targtype=zone,player=player,season=season)
        if car != None:
            return car.rushing_att
        else:
            return int('0') 
    def targets(self,player,zone,season):
        tar = self.playerstats(targtype=zone,player=player,season=season)
        if tar != None:
            return tar.receiving_tar
        else:
            return int('0')
    def completions(self,player,zone,season):
        comp = self.playerstats(targtype=zone,player=player,season=season)
        if comp != None:
            return int(comp.passing_cmp)
        else:
            return int('0')

    def qboppurtunity(self,player,season):
        fp = ['non-redzone','redzone','goaline1','goaline2','goaline3']
        stats = {}
        for x in fp:
            comp = self.completions(player,x,season)
            stats[x] = {}
            stats[x]['completions'] = comp
        nrzcomp = stats['non-redzone']['completions'] * 1.07
        rzcomp = stats['redzone']['completions'] * 2.63
        gl1comp = stats['goaline1']['completions'] * 4.69
        gl2comp = stats['goaline2']['completions'] * 7.09
        gl3comp = stats['goaline3']['completions'] * 8.00
        return nrzcomp + rzcomp + gl1comp + gl2comp + gl3comp
    
    def flexoppurtunity_index(self,player,season):
        fp = ['non-redzone','redzone','goaline1','goaline2','goaline3']
        stats = {}
        for x in fp:
            carries = self.carries(player,x,season)
            targets = self.targets(player,x,season)
            stats[x] = {}
            stats[x]['carries'] = int(carries)
            stats[x]['targets'] = int(targets)
        nrzcarries = stats['non-redzone']['carries']
        rzcarries = stats['redzone']['carries'] * 1.35
        gl1carries = stats['goaline1']['carries'] * 2.03
        gl2carries = stats['goaline2']['carries'] * 3.79
        gl3carries = stats['goaline3']['carries'] * 6.66
        nrztargets = stats['non-redzone']['targets'] * 1.84
        rztargets = stats['redzone']['targets'] * 2.83
        gl1targets = stats['goaline1']['targets'] * 4.31
        gl2targets = stats['goaline2']['targets'] * 5.41
        gl3targets = stats['goaline3']['targets'] * 6.58

        return nrzcarries + rzcarries + gl1carries + gl2carries + gl3carries + nrztargets + rztargets + gl1targets + gl2targets + gl3targets
    def games_played(self,player,year):
        db = nfldb.connect()
        q = nfldb.Query(db)
        q.game(season_year=year, season_type='Regular',)
        q.player(full_name=player)
        if q.as_games() != None:
            return len(q.as_games())
        else:
            return 0
    
    def top_oppscore(self,players,pos,numresults):
        playerlst = []
        stats = []
        if pos !='DST':
            for x in players:
                if players[x]['Position'] == pos:
                    playerlst.append(x)
            for x in playerlst:
                stats.append((x,players[x]['Oppscore']))
                if len(stats) > numresults:
                    stats = sorted(stats, key=lambda x: x[1],reverse=True)
                    stats.pop()
        return stats
    def top_value(self,players,pos,numresults):
        playerlst = []
        stats = []
        if pos !='DST':
            for x in players:
                if players[x]['Position'] == pos:
                    playerlst.append(x)
            for x in playerlst:
                if float(players[x]['AvgPointsPerGame']) > 10 and players[x]['Oppscore'] > 15:
                    stats.append((x,players[x]['Value']))
                if len(stats) > numresults:
                    stats = sorted(stats, key=lambda x: x[1])
                    stats.pop()
        return sorted(stats, key=lambda x: x[1])

        


        




