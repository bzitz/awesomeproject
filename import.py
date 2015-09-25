import team, json

new_players = team.Player('pos')
new_team = team.Team()
new_players.import_json()
#new_team.import_data()
#new_team.add_value()
new_players.update_ptsperopp()
new_players.update_ranks()
new_players.player_rating()
#
json_file = open('dkplayers.json', 'w')
json_file.write(json.dumps(new_players.players,indent=2))
json_file.close()
