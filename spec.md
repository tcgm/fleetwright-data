> **The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).**

Ships and ship classes are stored in YAML format.  You should probably just read the examples at the bottom.

`.fwship` and `.fwclass` files MUST be valid [YAML](https://yaml.org). since YAML is a superset of JSON, they *could* be [JSON](https://json.org), but they SHOULD NOT.

We're using [TypeScript Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html) to describe the format, because at least I find it intuitive.
You're not expected to actually load these at runtime or anything (although you *could*); understand them with your brain and use the information to write your app.

Applications MAY reject a ship/class with unknown components, or MAY display them as errors, or MAY try to find the prototypes in some sort of database.

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
    modules?: {
        crew?: CrewModule[],
        buffs?: BuffModule[],                    // \_ also mutex for now
        leveled_buffs?: LeveledBuffModule[],     // /
        converter?: ConverterModule[],           // \
        engine?: EngineModule[],                 //  |
        tank?: TankModule[],                     //  |
        combat_station?: CombatStationModule[],  //  |> Mutually exclusive for now
        quarters?: QuartersModule[],             //  |   applications MAY support it 
        recreational?: RecreationModule[],       //  |   but the behaviour is technically undefined 
        weapon_direct?: WeaponDirectModule[],    //  |  also undefined behaviour, but MAY be supported:
        weapon_guided?: WeaponGuidedModule[],    //  |   more than one of the same module
        ftl_drive?: FTLDriveModule[],            // /
    }
}

// ...
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
        base?: int,
        per_volume?: int,
    },
}

type BuffModule = {
    // #TODO
}

type ConverterModule = {
    input: Object<str,int>, // resource: amount
    outupt: Object<str,int>,
}

type EngineModule = {
    thrust: int,
    heat: int,
    fuel: string, // resource
    fuel_flow: int, // fuel/turn
}

type TankModule = {
    stores: string, // resource
}

type CombatStationModule = {
    // #TODO
}

type QuartersModule = {
    crew: int, // /volume
    morale: int
}

type RecreationalModule = {
    crew: int, // /volume
    morale: int,
}

type LeveledBuffModule = {
    levels: {
        1: {/* #TODO */}
        2: {/* #TODO */}
        3: {/* #TODO */}
        4: {/* #TODO */}
        // etc
    }
}

type WeaponDirectModule = {
    // #TODO
}

type WeaponGuidedModule = {
    // #TODO
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


### Component Details
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

## `.fwship`
```ts
type ShipInstance = {
    type: "ship",
    name: string,
    description: ?string, //shown to other players
    notes: ?string, // private to owner, MAY be viewable by DM. multiline MUST be allowed.
    created?: ?str // RFC 3339, (i.e., allows a space instead of 'T')
    edited?: ?str 
    armour_mass: int,
    components: FleetwrightComponentInstance[],
}
```

## `.fwclass`
```ts
type ShipClass = {
    type: "ship_class",
    name: string,
    description: ?string,
    notes: ?string, 
    created?: ?str // RFC 3339, (i.e., allows a space instead of 'T')
    edited?: ?str 
    components: FleetwrightComponentInstance[],
}
```

## Examples

**`pegasus.fwship`**
```yaml
name: "Pegasus"
description: "Lead ship of the Pegasus-class"
components: [
    {
        id: "fissile_salt_water",
        type: "drive",
        volume: 10,
        armour: true,
    },{
        id: "fission_fragment",
        type: "powerplant",
        volume: 4,
        armour: true,
    }
]
# ...
```

**`newsflash.fwclass`**
```yaml
name: "Newsflash-Class"
description: "Courier ship"
notes: "asduhfakodasdbaposdfi"
components:
    # yes this is valid yaml, all one library i checked outputs like this by default actually
    # it parses the same as the ship above
  - id: "fusion_torch"
    type: "drive"
    volume: 2
    armour: false
  - id: "electrostatic_fusion"
    type: "powerplant"
    volume: 4
    armour: false
```

**`plasma_cannon.fwcomponent`**
```yaml
id: "plasma_cannon",
type: "weapon",
# #TODO
```