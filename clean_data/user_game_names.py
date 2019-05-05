import ast
import json

filepath = './user_items.json'
writefilepath = './user_game_names.csv'

# max_game_id = 99920 for 100k cap
# 				= 19990 for 20k cap
# total cap is 530720
data = []

with open(filepath) as f:
	for line in f:
		l = ast.literal_eval(line)	# Convert single quotes in json to proper double quotes

		# Don't consider a user that doesn't own any games
		if int(l["items_count"]) > 0:		
			games = l["items"]
			games_filter = []
			for g in games:
				playtime = g["playtime_forever"]
				if playtime > 0:	# Also don't consider games not played
					game_id = int(g["item_id"])
					if game_id <= 100000: 		# Set limit on games due to space
						games_filter.append(g["item_name"])
			data.append({l["user_id"]: games_filter})

with open(writefilepath, 'w') as outfile:
	outfile.write(
		'[' +
		',\n'.join(json.dumps(i) for i in data) +
		']\n')