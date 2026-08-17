import json, os
p = r"kodi_data\profile\addon_data\plugin.video.palantir3\settings.json"
if os.path.exists(p):
    with open(p, "w") as f:
        json.dump({"Alldebrid_enabled": False, "Alldebrid_apikey": ""}, f)
    print("Reset settings.json successfully!")
