import nfldb

db = nfldb.connect()
q = nfldb.Query(db)
q.player(full_name="Eric Martin")
for guy in q.as_players():
    print guy.team
