const glob = require("glob");
const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");
const AdmZip = require("adm-zip");

// Gamedata master directory
const DATA_DIR = "gamedata/";

// Vanilla Gamedata Processing
const BASEDATA_DIR = DATA_DIR + "fleetwright/";

const BASE_DIRECTORIES = [
  "components",
  "missiles",
  "stations",
  "resources",
];

let filenames = [];
for (const directory of BASE_DIRECTORIES) {
  filenames = filenames.concat(
    glob.sync(`${BASEDATA_DIR + directory}/**/*.fw`, { recursive: true })
  );
}

const result = {
  resources: {},
  components: {},
  combat_stations: {},
  missiles: {},
};

for (const filename of filenames) {
  console.log(`${filename}...`);
  const current = yaml.safeLoad(fs.readFileSync(filename, "utf8"));
  if ("resources" in current) {
    Object.assign(result.resources, current.resources);
  }
  if ("component" in current) {
    Object.assign(result.components, current.component);
  }
  if ("components" in current) {
    Object.assign(result.components, current.components);
  }
  if ("missile" in current) {
    Object.assign(result.missiles, current.missile);
  }
  if ("missiles" in current) {
    Object.assign(result.missiles, current.missiles);
  }
  if ("combat_station" in current) {
    Object.assign(result.combat_stations, current.combat_station);
  }
  if ("combat_stations" in current) {
    Object.assign(result.combat_stations, current.combat_stations);
  }
}

fs.writeFileSync("junctspace.yaml", yaml.safeDump(result, { sortKeys: false }));

fs.writeFileSync("junctspace.txt", yaml.safeDump(result, { sortKeys: false }));

fs.writeFileSync("junctspace.fw", yaml.safeDump(result, { sortKeys: false }));

fs.writeFileSync(
  "junctspace_dump.yaml",
  yaml.safeDump(result, { sortKeys: false })
);

fs.writeFileSync(
  "junctspace_dump.txt",
  yaml.safeDump(result, { sortKeys: false })
);

fs.writeFileSync(
  "junctspace_dump.fw",
  yaml.safeDump(result, { sortKeys: false })
);

const zip = new AdmZip();
for (const filename of filenames) {
  zip.addLocalFile(path.resolve(filename));
}
zip.writeZip("fleetwright.zip");
