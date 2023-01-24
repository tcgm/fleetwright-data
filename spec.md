> **The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).**

Ships and ship classes are stored in YAML format.  You should probably just read the examples at the bottom.

`.fwship` and `.fwclass` files MUST be valid [YAML](https://yaml.org). since YAML is a superset of JSON, they *could* be [JSON](https://json.org), but they SHOULD NOT.

We're using [TypeScript Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html) to describe the format, because at least I find it intuitive.
You're not expected to actually load these at runtime or anything (although you *could*); understand them with your brain and use the information to write your app.

Applications MAY reject a ship/class with unknown components, or MAY display them as errors, or MAY try to find the prototypes in some sort of database.

## Shared Types

```ts
type CrewingRequirements = {
    strategic?: { // 0 if missing. SHOULD be displayed to the user as "maintenance"
        base: int
        per_volume: int
    },
    tactical?: { // 0 if missing. SHOULD be displayed to the user as "combat"
        base: int
        per_volume: int
    }
}

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
    crew?: ?CrewingRequirements, // no crew required if missing
    scaling_method?: "volume" | "leveled", // "volume" if missing
    // #TODO level info
    // #TODO upgrade point info (for weapons)
}

// ...
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