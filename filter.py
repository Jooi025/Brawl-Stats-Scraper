import json

with open("raw_stats.json") as f:
    data = json.load(f)

    for name,allStats in data.items():
        for category, stats in list(allStats.items()):
            # get the desire stats and does the dictionary need to be changed
            if category == "Base":
                valid = ["Base health","Movement speed"]
                change = False

            elif "Attack: " in category:
                newKey = "Attack"
                valid = ["Range","Reload time","Max. ammo"]
                change = True
            
            elif "Super" in category:
                newKey = "Super"
                valid = ["Range"]
                change = True
            else:
                # delete the category that is not needed
                del allStats[category]
                change = False

            # change the key 
            if change:
                allStats[newKey] = allStats[category]
                del allStats[category]

            # float the string 
            for stat, value in list(stats.items()):
                if (stat in valid):
                    try:
                        stats[stat] = float(value)
                    except ValueError:
                        stats[stat] = float(value.split(" ")[0])
                else:
                    # delete the stat that is not needed
                    del stats[stat]

# make a new filtered json
with open("filter_stats.json", "w") as f:
    jsonObject = json.dumps(data, indent=4)
    f.write(jsonObject)