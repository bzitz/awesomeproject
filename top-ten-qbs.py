import nfldb, team, stats
from tabulate import tabulate

def get_weights(fieldposition):
    db = nfldb.connect()
    q = nfldb.Query(db)
    if fieldposition == "non-redzone":
        startpos = "OWN 1"
        endpos = "OPP 21"
    elif fieldposition == "redzone":
        startpos = "OPP 20"
        endpos = "OPP 11"
    elif fieldposition == "goaline1":
        startpos = "OPP 10"
        endpos = "OPP 6"
    elif fieldposition == "goaline2":
        startpos = "OPP 5"
        endpos = "OPP 3"
    elif fieldposition == "goaline3":
        startpos = "OPP 2"
        endpos   = "OPP 1"

    pos1 = nfldb.FieldPosition.from_str(startpos)
    pos2 = nfldb.FieldPosition.from_str(endpos)
    q.game(season_year=2015, season_type='Regular')
    q.play(yardline__ge=pos1)
    q.play(yardline__le=pos2)

    rushtotal = 0
    passtotal = 0
    target = 0
    pts = 0
    passpts = 0
    recpts = 0
    for game in q.as_play_players():
        if game.rushing_att:
            rushtotal = rushtotal + 1
            if game.rushing_yds > 0:
                pts = pts + (game.rushing_yds * .1)
            if game.fumbles_lost:
                pts = pts - 1
            if game.rushing_tds:
                pts = pts + 6
        if game.passing_att:
            passtotal = passtotal + 1
            if game.passing_yds:
                passpts = passpts + (game.passing_yds * .04)
            if game.passing_tds:
                passpts = passpts + 4
            if game.passing_int:
                passpts = passpts - 1
            if game.fumbles_lost:
                passpts = recpts - 1
        if game.receiving_tar:
            target = target + 1
            if game.receiving_yds:
                recpts = recpts + (game.receiving_yds * .1)
            if game.receiving_rec:
                recpts = recpts + 1
            if game.fumbles_lost:
                recpts = recpts - 1
            if game.receiving_tds:
                recpts = recpts + 6

    print  "rushing", pts/rushtotal, rushtotal
    print  "passing", passpts/passtotal, passtotal
    print  "receiving", recpts/target, target


def get_fantasypoints(year, player):
    db = nfldb.connect()
    q = nfldb.Query(db)
    x = nfldb.Query(db)
    q.game(season_year=year, season_type='Regular')
    q.player(full_name=player)
    results = []
    for p in q.as_players():
        team = p.team
    for game in q.as_games():
        if game.home_team == team:
            opp =  game.away_team
        if game.away_team == team:
            opp = game.home_team
        week = game.week
        results.append((player, week, opp, get_weeklypoints(year,player,week)))
    return results

def get_weeklypoints(year, player, week):
    db = nfldb.connect()
    x = nfldb.Query(db)
    x.game(season_year=year, week=week, season_type='Regular')
    x.player(full_name=player)
    pts = 0
    for game in x.as_aggregate():
        if game.fumbles_lost:
            pts = pts - 1
        if game.puntret_tds:
            pts = pts + 6
        if game.fumbles_rec_tds:
            pts = pts + 6
        if game.rushing_att:
            if game.rushing_yds:
                pts = pts + (game.rushing_yds * .1)
                if game.rushing_yds > 100:
                    pts = pts + 3
            if game.rushing_tds:
                pts = pts + (game.rushing_tds * 6)
            if game.rushing_twoptm:
                pts = pts + (game.rushing_twoptm * 2)
        if game.passing_att:
            if game.passing_yds:
                pts = pts + (game.passing_yds * .04)
                if game.passing_yds > 300:
                    pts = pts + 3
            if game.passing_tds:
                pts = pts + (game.passing_tds * 4)
            if game.passing_int:
                pts = pts - 1
            if game.passing_twoptm:
                pts = pts + (game.passing_twoptm * 2)
        if game.receiving_tar:
            if game.receiving_yds:
                pts = pts + (game.receiving_yds * .1)
                if game.receiving_yds > 100:
                    pts = pts + 3
            if game.receiving_rec:
                pts = pts + game.receiving_rec
            if game.receiving_tds:
                pts = pts + (6 * game.receiving_tds)
            if game.receiving_twoptm:
                pts = pts + (2 * game.receiving_twoptm)
    return pts
 

def get_ptsagainst(team, year):
    db = nfldb.connect()
    q = nfldb.Query(db)
    results = []
    q.game(season_year=year, season_type='Regular', team=team )
    for game in q.as_games():
        if game.finished:
            if game.home_team == team:
                opp = game.away_team
            elif game.away_team == team:
                opp = game.home_team
            players = get_weeklypts(opp,game.week,year)
            for x in players:
                results.append(x)
    return results

def get_weeklypts(team, week, year):
    players = []
    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=year, season_type='Regular', team=team, week=week )
    for p in q.as_players():
        if p.team == team and p.team != "UNK":  
            pts = get_weeklypoints(year,p.full_name, week)
            if pts != 0:
                players.append((p.full_name,str(p.position),str(p.team), week, pts)) 
                
    return players

def display_ptsagainst(team, year):
    data = get_ptsagainst(team,year)
    weeks = []
    for x in data:
        if x[3] not in weeks:
            weeks.append(x[3])

    tqb = 0
    trb = 0
    twr = 0
    tte = 0

    for week in sorted(weeks):
        teamtable = []
        qb = 0 
        rb = 0
        wr = 0
        te = 0
        for x in data:
            if x[3] == week:
                playertable = [x[0],x[1],x[2],x[4]]
                teamtable.append(playertable)
                if x[1] == "RB":
                    rb = rb + x[4]
                    trb = trb + x[4]
                if x[1] == "QB":
                    qb = qb + x[4]
                    tqb = tqb + x[4]
                if x[1] == "WR":
                    wr = wr + x[4]
                    twr = twr + x[4]
                if x[1] == "TE":
                    te = te + x[4]
                    tte = tte + x[4]
        total = qb + rb + wr + te
        print "\n"
        print "Week %s" % week
        print tabulate(teamtable, headers = ["Name", "Position","Team","Pts"])
        print "\n"
        print tabulate([["QB",qb],["RB",rb],["WR",wr],["TE",te],["Total",total]], headers = ["Position","Pts"])
    overall = tqb + trb + twr + tte
    print "\n"
    print "Season Averages"        
    print tabulate([["QB",tqb/len(weeks)],["RB",trb/len(weeks)],["WR",twr/len(weeks)],["TE",tte/len(weeks)],["Total",overall/len(weeks)]], headers = ["Position","Pts"])

def display_playerpts(year, player):
    data = get_fantasypoints(year, player)
    weeks = []
    for x in data:
        weeks.append([x[1],x[2],x[3]])
    print tabulate(weeks,headers = ["Week","Opponent","Points"])

def display_playervalue(pos, numresults):
    val = []
    st = stats.Stats()
    p = team.Player('pos')
    p.import_json()
    data = st.top_value(p.players,pos,numresults)
    for x in data:
        val.append([x[0],x[1],p.players[x[0]]['Oppscore'],p.players[x[0]]['Oppscorerank']])
    print tabulate(val, headers = ["Player", "Value", "Oppurtunity", "Opp Rank"])


display_playervalue('QB', 30)
display_playervalue('RB', 30)
display_playervalue('WR', 30)
display_playervalue('TE', 30)


