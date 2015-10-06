import team, json

new_team = team.Team('qb','rb1','rb2','wr1','wr2','wr3','te','flex', 'dst')
new_team.import_data()
new_team.add_value()
new_team.remove_zeros()
#
json_file = open('dkplayers.json', 'w')
json_file.write(json.dumps(new_team.players,indent=2))
json_file.close()

new_players = team.Player('pos')
new_players.import_json()
new_players.update_ptsperopp()
new_players.update_ranks()
new_players.player_rating()
#
json_file = open('dkplayers.json', 'w')
json_file.write(json.dumps(new_players.players,indent=2))
json_file.close()
