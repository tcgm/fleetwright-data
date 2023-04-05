import glob
import yaml
import pprint
import os
import zipfile

BASE_DIRECTORIES = [
    "components",
    "missiles",
    "stations",
    "resources",
]

filenames = []
for directory in BASE_DIRECTORIES:
    filenames.extend(
        glob.glob(f"{directory}/**/*.fw", recursive=True)
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

with open("junctspace.txt", "w") as f:
    yaml.dump(result, f, Dumper=yaml.SafeDumper, sort_keys=False)

with open("junctspace.fw", "w") as f:
    yaml.dump(result, f, Dumper=yaml.SafeDumper, sort_keys=False)

with open("junctspace_dump.yaml", "w") as f:
    yaml.dump(result, f, Dumper=yaml.SafeDumper, sort_keys=False)

with open("junctspace_dump.txt", "w") as f:
    yaml.dump(result, f, Dumper=yaml.SafeDumper, sort_keys=False)

with open("junctspace_dump.fw", "w") as f:
    yaml.dump(result, f, Dumper=yaml.SafeDumper, sort_keys=False)

path = ""
zipf = zipfile.ZipFile('junctspace.zip'.format(os.path.join(path, directory)), 'w', zipfile.ZIP_DEFLATED)
for filename in filenames:
    zipf.write(os.path.abspath(filename), arcname=filename)
zipf.close()