# Fleetwright Specifications

there's no offical badge you get for complying to this spec or anything. if it works it works. but you probably should anyways.  
I sort of personally think all of these are Pretty Good&trade;

> **The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).**

Ships and ship classes are stored in YAML format.  You should probably just read the examples at the bottom.

`.fwship` and `.fwclass` files MUST be valid [YAML](https://yaml.org). since YAML is a superset of JSON, they *could* be [JSON](https://json.org), but they SHOULD NOT.

We're using [TypeScript Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html) to describe the format, because at least I find it intuitive.
You're not expected to actually load these at runtime or anything (although you *could*); understand them with your brain and use the information to write your app.

- Applications SHOULD reatin components they don't understand
    - they MAY display them as warnings
    - they MAY guess that the component has density 1, cost 1, durability 1
    - they MAY allow the user to write-in the desnity, cost, and durability
    - they MAY attempt to find the prototype in some sort of mod database
- Applications SHOULD retain ship properties which they doesn't understand.
- Applications MUST NOT require that a ship class be provided to use a ship instance.
    - this is because i think most users won't want to bother faffing about with ship classes, they'll just create 10 copies of a ship with changed names
    - no *forcing* the user to make a class which they then have to think about
    - if on the backend you need the class to exist, you can transparently create a class and have the user secretly be editing that
    - but you still have to let them save only the ship
- Applications SHOULD handle duplicate UUIDs gracefully
    - prompt the user to make a copy or something like that
    - or as long as the name is different you can just pick a new uuid


## Components
```ts
type ComponentInstance = {
    id: string,
    volume: int,
    armour: bool,
    notes: ?string, // private to owner, MAY be viewable by DM. multiline MUST be allowed.
    assigned_crew?: null, // #TODO
    details: TankDetails | DirectWeaponDetails | GuidedWeaponDetails, // etc
}

type ComponentPrototype = {
    // id given by dict key
    type: string,
    name?: ?string,
    description?: ?string,
    density: int,
    durability: int,
    price: int,
    fixed_volume?: int, // e.g., bridges have this =1. scaling still applies!
    modules?: ModuleObject,
}

type ModuleObject = {
    crew?: CrewModule,
    buffs?: BuffModule,                    // \_ also mutex for now
    leveled_buffs?: LeveledBuffModule,     // /
    converter?: ConverterModule,           // \
    engine?: EngineModule,                 //  |
    storage?: StorageModule,               //  |
    combat_station?: CombatStationModule,  //  |> Mutually exclusive for now
    quarters?: QuartersModule,             //  |   applications MAY support it 
    stores?: StoresModule,                 //  |   but the behaviour is technically undefined 
    recreational?: RecreationModule,       //  |
    command: CommandModule,                //  |
    weapon_direct?: WeaponDirectModule,    //  |
    weapon_guided?: WeaponGuidedModule,    //  |   
    ftl_drive?: FTLDriveModule,            // /
}
```

### Modules
```ts
type CrewModule = {
    strategic?: {
        // e.g., maintenance crew
        base?: int,
        per_volume?: int,
    },
    tactical?: {
        // combat crew
        base?: int,
        per_volume?: int,
    },
}

type BuffModule = {
    scaling_function?: 1 | "volume"; // maybe others, default volume
    stacking?: bool,   // default true
    add?: Object,      // stat: delta, default {}
    multiply?: Object, // stat: multiplier, default {}
}

type LevelledBuffModule = {
    
}

type ConverterModule = {
    input: Object<str,int>, // resource: amount
    outupt: Object<str,int>,
}

type EngineModule = {
    thrust: int,
    heat?: int,
    fuel: {[resource]: double},
    fuel_flow: int, // fuel/turn
}

type StorageModule = {
    stores: string, // resource
}

type QuartersModule = {
    crew: int, // /volume
    morale: int
}

type StoresModule = {
    crew: int // kept alive/turn/volume
    infinite?: bool,
    morale: int
}

type RecreationalModule = {
    crew_served: int, // /volume
    biological: int, // morale modifier
    construct: int,  // could technically be negative
    infomorph: int,  // but why would you want that?
}


type WeaponDirectModule = {
    // #TODO
}

type WeaponGuidedModule = {
    // #TODO
}

type CommandModule = {
    operate_offensive: bool,
    operate_defensive: bool,
    operate_navigation: bool,
}

type FTLDriveModule = {
    // #TODO non-jump ftl
    method: "linear" | "log",
    jump_tac_tidi: int,
    jump_tac_energy: int,
    jump_str_energy: int,
    jump_range: {
      method: "log" | "linear",
      constant: int,
      base: int, // "log" only
      multiplier: int,
    }
}
```


### Details
```ts
type TankDetails = {
    fill_level?: int, // app MAY reject if > volume, or MAY automatically fix. if missing, implicitly full.
}

type DirectWeaponDetails = {
    // #TODO upgrade points
}

type GuidedWeaponDetails = {
    // #TODO mixed silos
    guidance: str // #TODO write down the types somewhere
    warhead: str // #TODO ditto warheads
    propulsion: str // #TODO ditto propulsion
}
```

## Top-Level of Files

### `.fwship`
```ts
type ShipInstance = {
    type: "ship",
    ship_name: string,
    class_name?: ?string, // mostly for the user to look at
    ship_uuid?: ?string,
    class_uuid?: ?string,
    description: ?string, //shown to other players
    notes: ?string, // private to owner, MAY be viewable by DM. multiline MUST be allowed. MAY support Markdown.
    created?: ?str, // RFC 3339, (i.e., allows a space instead of 'T')
    edited?: ?str,  // ditto
    livery?: ?str,  // file path (how this is resolved is an implemention detail)
    image?: ?str,   // ditto
    armour_mass: int,
    components: FleetwrightComponentInstance[],
}
```

### `.fwclass`
```ts
type ShipClass = {
    type: "ship_class",
    class_name: string,
    class_uuid?: ?string, // preferably v4
    description: ?string, //shown to other players
    notes: ?string, // private to owner, MAY be viewable by DM. multiline MUST be allowed. MAY support Markdown.
    created?: ?str, // RFC 3339, (i.e., allows a space instead of 'T')
    edited?: ?str,  // ditto
    livery?: ?str,  // file path (how this is resolved is an implemention detail)
    image?: ?str,   // ditto
    components: FleetwrightComponentInstance[],
}
```

## Examples

**`dolphin.fwship`**
```yaml
%YAML 1.2
#%FLEETWRIGHT/SHIP 0.0.1
---
type: "ship"
name: "Inventive Dolphin"
class_name: "Pegasus"
armour: 372
components:
  - {id: "fissile_salt_water", volume: 10, armour: true}
  - {id: "tank_dissolved_fissiles", volume: 40, armour: true}
  - {id: "fission_fragment", volume: 4, armour: true}
  - {id: "fission_fragment", volume: 4, armour: true}
  - {id: "fission_fragment", volume: 2, armour: true}
  - {id: "tank_inert_fluid", volume: 4, armour: true}
  - {id: "tank_inert_fluid", volume: 4, armour: true}
  - {id: "open_cycle", volume: 2, armour: true}
  - {id: "open_cycle", volume: 2, armour: true}
  - {id: "shipmind_brainframe", volume: 1, armour: true}
  - {id: "shipmind_brainframe", volume: 1, armour: true}
  - {id: "damcon", volume: 1, armour: true}
  - {id: "damcon", volume: 1, armour: true}
  - {id: "engineering", volume: 1, armour: true}
  - {id: "nerve_center", volume: 1, armour: true}
  - {id: "medevac", volume: 1, armour: true}
  - {id: "particle_beam", volume: 24, armour: true}
  - {id: "macron_gun", volume: 8, armour: true}
  - {id: "macron_gun", volume: 8, armour: true}
  - {id: "jump_standard", volume: 15, armour: true}
  - {id: "jump_tactical", volume: 5, armour: true}
  - {id: "spartan", volume: 3, armour: true}
```

**`newsflash.fwclass`**
```yaml
%YAML 1.2
#%FLEETWRIGHT/CLASS 0.0.1
---
type: "ship_class"
name: "Newsflash-Class Courier"
armour: 0
components:
  - id: "fusion_torch"
    volume: 2
    armour: false
  - id: "electrostatic_fusion"
    volume: 4
    armour: false
  - id: "jump_longrange"
    volume: 19
    armour: true
  - id: "tank_d3he"
    volume: 1
    armour: false
  - id: "civilian_bridge"
    volume: 1
    armour: false

```

**`plasma_cannon.fwcomponent`**
```yaml
# #TODO
```