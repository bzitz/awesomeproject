import nfldb

db = nfldb.connect()
q = nfldb.Query(db)
opp20 = nfldb.FieldPosition.from_str('OPP 20')
opp10 = nfldb.FieldPosition.from_str('OPP 10')
q.game(season_year=2015, season_type='Regular')
q.player(full_name = "Ben Roethlisberger")


#q.play(pos_team = 'CAR' )
#q.player(full_name="T.J. Yeldon")
#q.player(team__ne='UNK')
total = 0

for game in q.as_aggregate():
    print game
