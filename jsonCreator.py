import json
import pandas as pd
import random
MOVIE_ID = 1

def recursive_len(item):
    if isinstance(item, (list,tuple,dict)):
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


df = pd.read_json('db_example.json')
print df._values

data = []
# forword on the users
for user in range(len(df._values)):
    # forword on the items
    for item in range(len(df._values[user][MOVIE_ID])):
        data.append({
        "user_id": user,
        "movie_id": df._values[user][0][item],
        "rating": df._values[user][1][item]
    })


with open('new_data.json', 'w') as outfile:
    json.dump(data, outfile)


