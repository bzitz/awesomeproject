import nfldb

def get_weights():
    db = nfldb.connect()
    q = nfldb.Query(db)
    pos1 = nfldb.FieldPosition.from_str('OPP 2')
    pos2 = nfldb.FieldPosition.from_str('OPP 1')
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
        print game
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

def get_fantasypoints(year, week, player):
    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=year, season_type='Regular', week=week)
    q.player(full_name=player)
    pts = 0  
    for game in q.as_aggregate():
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
                pts = pts + 6
            if game.receiving_twoptm:
                pts = pts + 2
    return pts
 

#get_fantasypoints(2015, 2, "Travis Benjamin")
def get_ptsagainst(year,week,team):
    players = []
    db = nfldb.connect()
    q = nfldb.Query(db)
    q.game(season_year=year, season_type='Regular', week=week, team=team )
    for game in q.as_players():
        if game.team != team:  
            pts = get_fantasypoints(year,week,game.full_name)
            if pts != 0:
                players.append((game.full_name,str(game.position),str(game.team), pts)) 
                
    print players
    total = 0
    for x in players:
        total = total + x[3] 
    print total
       
get_ptsagainst(2015,1,'WAS')
