import glob
import yaml
import pprint

BASE_DIRECTORIES = [
    "components",
    "missiles",
    "stations",
    "resources",
]

filenames = []
for directory in BASE_DIRECTORIES:
    filenames.extend(
        glob.glob(f"{directory}/*.fw")
    )
    filenames.extend(
        glob.glob(f"{directory}/**/*.fw")
    )

result = {
    "resources": {},
    "components": {},
    "combat_stations": {},
    "missiles": {},
}

for filename in filenames:
    print(f"{filename}...")
    with open(filename) as f:
        current = yaml.load(f, Loader=yaml.SafeLoader)
        if("resources" in current):
            result["resources"].update(
                current["resources"]
            )
        if("component" in current):
            result["components"].update(
                current["component"]
            )
        if("components" in current):
            result["components"].update(
                current["components"]
            )
        if("missile" in current):
            result["missiles"].update(
                current["missile"]
            )
        if("missiles" in current):
            result["missiles"].update(
                current["missiles"]
            )
        if("missiles" in current):
            result["missiles"].update(
                current["missiles"]
            )
        if("combat_station" in current):
            result["combat_stations"].update(
                current["combat_station"]
            )
        if("combat_stations" in current):
            result["combat_stations"].update(
                current["combat_stations"]
            )

with open("junctspace.yaml", "w") as f:
    yaml.dump(result, f, Dumper=yaml.SafeDumper, sort_keys=False)