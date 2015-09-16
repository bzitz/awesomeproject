import nfldb

db = nfldb.connect()
q = nfldb.Query(db)
opp20 = nfldb.FieldPosition.from_str('OPP 20')
q.game(season_year=2015, season_type='Regular', team = "CAR")
#q.play(pos_team = 'CAR' )
#q.player(full_name="T.J. Yeldon")
#q.player(team__ne='UNK')
total = 0
for game in q.as_plays():
    print len(q.as_plays())
    print game

