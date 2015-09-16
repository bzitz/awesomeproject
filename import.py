import team, json

new_team = team.Team()
new_team.import_data()
new_team.add_value()
print new_team.players

json_file = open('dkplayers.json', 'w')
json_file.write(json.dumps(new_team.players,indent=2))
json_file.close()
