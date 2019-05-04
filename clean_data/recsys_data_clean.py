import json
import pandas as pd
import ast

filepath = './user_items.json'
#writefilepath = './clean_user_items.json'
writefilepath = './user_items_matrix.csv'


data = []
max_item_id = 0
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
						if game_id > max_item_id:
							max_item_id = game_id
						games_filter.append({game_id: playtime})
			data.append({l["user_id"]: games_filter})

print(max_item_id)

# Intermediate data written out (not much use without a little more profiling; we still need max_item_id)
#with open(writefilepath, 'w') as outfile:
#	json.dump(data, outfile)

# Now with format as data (list of nested JSON objects) = 	[	{user_id: [	{item_id: playtime_forever}		]	}	]
# Convert to dataframe where
#		item_id		0		..		max_item_id		
#  user_id 			
#	x1				playtime_forever
#	...
#	xn


df = pd.DataFrame(columns = list(range(max_item_id)))

for user in data:
	key = next(iter(user))	# Note there's only one key. User is {user_id: [...]}
		items = user[key]
		items_list = [0] * max_item_id
		for i in items:
			[(k, v)] = i.items()
			items_list[k] = v
		df[key] = items_list

df.head(10)
df.to_csv(writefilepath)
