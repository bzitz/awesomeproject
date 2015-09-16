import nfldb

db = nfldb.connect()
q = nfldb.Query(db)
opp20 = nfldb.FieldPosition.from_str('OPP 20')
q.game(season_year=2015, season_type='Regular')
#q.play(yardline__ge=opp20)
q.player(full_name="Odell Beckham")
#q.player(team__ne='UNK')
total = 0
for game in q.as_aggregate():
    total = total + (game.rushing_att + game.receiving_tar)
print game, total

