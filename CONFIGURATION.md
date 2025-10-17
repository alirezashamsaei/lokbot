# Lok Bot Configuration Documentation

## Overview

The lok_bot configuration system uses two main execution models:

- **Jobs**: Scheduled tasks that run at specific intervals
- **Threads**: Continuous background processes that monitor and respond to events

## Jobs vs Threads

### Jobs (Scheduled Tasks)
- **Purpose**: Handle periodic maintenance tasks
- **Execution**: Run at specific time intervals (e.g., every 120-200 minutes)
- **Examples**: Claiming rewards, harvesting resources, alliance activities
- **Configuration**: Each job has an `interval` with `start` and `end` minutes

### Threads (Continuous Background Processes)
- **Purpose**: Monitor and respond to events in real-time
- **Execution**: Run continuously in the background
- **Examples**: Building upgrades, research, troop training, quest monitoring
- **Configuration**: No interval specified - they run continuously

## Configuration Structure

```json
{
  "main": {
    "jobs": [...],      // Scheduled tasks
    "threads": [...]    // Continuous background processes
  },
  "socketio": {
    "debug": false      // WebSocket debugging
  }
}
```

## Jobs Configuration

### 1. `hospital_recover`
**Purpose**: Automatically recovers wounded troops in the hospital
- **Interval**: 90-180 minutes
- **Function**: Checks hospital for wounded troops and uses recovery items
- **Parameters**: None
- **Dependencies**: Requires hospital building and recovery items

### 2. `wall_repair`
**Purpose**: Repairs castle walls when damaged
- **Interval**: 30-90 minutes
- **Function**: Checks wall durability and repairs if needed
- **Parameters**: None
- **Dependencies**: Requires wall building and repair resources

### 3. `alliance_farmer`
**Purpose**: Manages alliance-related activities
- **Interval**: 120-200 minutes
- **Parameters**:
  - `gift_claim` (boolean): Claim alliance gifts
  - `help_all` (boolean): Help alliance members with construction/research
  - `research_donate` (boolean): Donate to alliance research
  - `shop_auto_buy_item_code_list` (array): Items to auto-buy from alliance shop
- **Dependencies**: Must be in an alliance

### 4. `mail_claim`
**Purpose**: Claims all types of mail rewards
- **Interval**: 120-200 minutes
- **Function**: Claims report, alliance, and system mail
- **Parameters**: None
- **Dependencies**: None

### 5. `caravan_farmer`
**Purpose**: Buys items from the caravan
- **Interval**: 120-200 minutes
- **Function**: Automatically purchases available caravan items
- **Parameters**: None
- **Dependencies**: Requires caravan and sufficient resources

### 6. `use_resource_in_item_list`
**Purpose**: Uses resource items from inventory
- **Interval**: 120-200 minutes
- **Function**: Automatically uses resource items (food, lumber, stone, gold)
- **Parameters**: None
- **Dependencies**: Requires resource items in inventory

### 7. `vip_chest_claim`
**Purpose**: Claims VIP daily chest
- **Interval**: 120-200 minutes
- **Function**: Claims daily VIP rewards
- **Parameters**: None
- **Dependencies**: Requires VIP status

### 8. `harvester`
**Purpose**: Harvests resources from buildings
- **Interval**: 10-20 minutes
- **Function**: Collects resources from farms, lumber camps, quarries, gold mines
- **Parameters**: None
- **Dependencies**: Requires resource buildings

### 9. `socf_thread` (Special Job)
**Purpose**: Field farming - searches for and attacks field objects
- **Interval**: 1 minute
- **Parameters**:
  - `targets` (array): Objects to search for (crystal mines, goblins, etc.)
  - `radius` (number): Search radius in zones
  - `share_to` (object): Chat channels to share findings
- **Dependencies**: Requires troops and march capacity

## Threads Configuration

### 1. `free_chest_farmer_thread`
**Purpose**: Claims free chests (silver, gold, platinum)
- **Execution**: Continuous monitoring
- **Function**: Automatically claims available free chests
- **Parameters**: None
- **Dependencies**: None

### 2. `quest_monitor_thread`
**Purpose**: Monitors and claims quest rewards
- **Execution**: Continuous monitoring
- **Function**: Automatically claims completed quest rewards
- **Parameters**: None
- **Dependencies**: None

### 3. `building_farmer_thread`
**Purpose**: Continuously upgrades buildings
- **Execution**: Continuous monitoring
- **Parameters**:
  - `speedup` (boolean): Use speedup items for building upgrades
- **Function**: Automatically starts building upgrades when workers are available
- **Dependencies**: Requires building workers and resources

### 4. `academy_farmer_thread`
**Purpose**: Continuously researches academy technologies
- **Execution**: Continuous monitoring
- **Parameters**:
  - `to_max_level` (boolean): Research to maximum level vs minimum required
  - `speedup` (boolean): Use speedup items for research
- **Function**: Automatically starts research when academy is available
- **Dependencies**: Requires academy building and research workers

### 5. `train_troop_thread`
**Purpose**: Continuously trains troops
- **Execution**: Continuous monitoring
- **Parameters**:
  - `troop_code` (number): Type of troop to train (e.g., 50100101 for Fighter)
  - `speedup` (boolean): Use speedup items for training
  - `interval` (number): Time between training cycles (default: 3600 seconds)
- **Function**: Automatically trains troops when barracks are available
- **Dependencies**: Requires barracks and training resources

## SocketIO Configuration

### `socketio.debug`
**Purpose**: Enables WebSocket debugging
- **Type**: Boolean
- **Default**: false
- **Function**: Controls WebSocket connection logging
- **Usage**: Set to true for troubleshooting connection issues

## Key Differences Summary

| Aspect | Jobs | Threads |
|--------|------|---------|
| **Execution Model** | Scheduled intervals | Continuous background |
| **Timing** | Specific intervals (e.g., 120-200 min) | Always running |
| **Purpose** | Periodic maintenance | Real-time monitoring |
| **Resource Usage** | Lower (runs occasionally) | Higher (always active) |
| **Response Time** | Delayed (next scheduled run) | Immediate |
| **Examples** | Claim rewards, harvest resources | Monitor buildings, research, quests |

## Configuration Best Practices

1. **Jobs**: Use for tasks that don't need immediate attention (daily rewards, resource collection)
2. **Threads**: Use for time-sensitive tasks (building upgrades, research, troop training)
3. **Intervals**: Balance between efficiency and responsiveness
4. **Dependencies**: Ensure required buildings and resources are available
5. **Speedup**: Use speedup items for faster progression (requires inventory items)

## Example Configuration

Here's a complete example configuration with all features enabled:

```json
{
  "main": {
    "jobs": [
      {
        "name": "hospital_recover",
        "enabled": true,
        "interval": {
          "start": 90,
          "end": 180
        }
      },
      {
        "name": "wall_repair",
        "enabled": true,
        "interval": {
          "start": 30,
          "end": 90
        }
      },
      {
        "name": "alliance_farmer",
        "enabled": true,
        "kwargs": {
          "gift_claim": true,
          "help_all": true,
          "research_donate": true,
          "shop_auto_buy_item_code_list": [10101008]
        },
        "interval": {
          "start": 120,
          "end": 200
        }
      },
      {
        "name": "mail_claim",
        "enabled": true,
        "interval": {
          "start": 120,
          "end": 200
        }
      },
      {
        "name": "caravan_farmer",
        "enabled": true,
        "interval": {
          "start": 120,
          "end": 200
        }
      },
      {
        "name": "use_resource_in_item_list",
        "enabled": true,
        "interval": {
          "start": 120,
          "end": 200
        }
      },
      {
        "name": "vip_chest_claim",
        "enabled": true,
        "interval": {
          "start": 120,
          "end": 200
        }
      },
      {
        "name": "harvester",
        "enabled": true,
        "interval": {
          "start": 10,
          "end": 20
        }
      },
      {
        "name": "socf_thread",
        "enabled": true,
        "kwargs": {
          "targets": [
            {
              "code": 20100105,
              "level": [1]
            },
            {
              "code": 20100106,
              "level": []
            },
            {
              "code": 20200101,
              "level": []
            },
            {
              "code": 20200102,
              "level": []
            }
          ],
          "radius": 8,
          "share_to": {
            "chat_channels": [1, 2]
          }
        },
        "interval": {
          "start": 1,
          "end": 1
        }
      }
    ],
    "threads": [
      {
        "name": "free_chest_farmer_thread",
        "enabled": true
      },
      {
        "name": "quest_monitor_thread",
        "enabled": true
      },
      {
        "name": "building_farmer_thread",
        "enabled": true,
        "kwargs": {
          "speedup": true
        }
      },
      {
        "name": "academy_farmer_thread",
        "enabled": true,
        "kwargs": {
          "to_max_level": false,
          "speedup": true
        }
      },
      {
        "name": "train_troop_thread",
        "enabled": true,
        "kwargs": {
          "troop_code": 50100101,
          "speedup": true,
          "interval": 3600
        }
      }
    ]
  },
  "socketio": {
    "debug": false
  }
}
```

## Troop Codes Reference

| Troop Name | Code | Tier |
|------------|------|------|
| Fighter | 50100101 | 1 |
| Hunter | 50100201 | 1 |
| Stable Man | 50100301 | 1 |
| Warrior | 50100102 | 2 |
| Longbow Man | 50100202 | 2 |
| Horseman | 50100302 | 2 |
| Knight | 50100103 | 3 |
| Ranger | 50100203 | 3 |
| Heavy Cavalry | 50100303 | 3 |
| Guardian | 50100104 | 4 |
| Crossbow Man | 50100204 | 4 |
| Iron Cavalry | 50100304 | 4 |
| Crusader | 50100105 | 5 |
| Sniper | 50100205 | 5 |
| Dragon | 50100305 | 5 |

## Complete Object Codes Reference

This section provides a comprehensive reference for all field objects and monsters that can be targeted by the bot's field farming system (`socf_thread`).

### Object Categories

- **Resource Objects**: Basic resource production buildings (farms, mines, etc.)
- **Battlefield Resource Objects**: Special battlefield versions of resource buildings
- **Special Buildings**: Unique structures like kingdoms, shrines, and alliance buildings
- **Gates and Fortresses**: Transportation and defensive structures
- **Charms**: Special items that can be found in the field
- **Monsters**: Hostile creatures that can be attacked for loot

### Resource Objects

| Object Name | Code | Type | Description |
|-------------|------|------|-------------|
| Farm | 20100101 | Resource | Food production building |
| Forest | 20100102 | Resource | Lumber production building |
| Quarry | 20100103 | Resource | Stone production building |
| Gold Mine | 20100104 | Resource | Gold production building |
| Crystal Mine | 20100105 | Resource | Crystal production building |
| Sealed Mine | 20100106 | Resource | Dragon Soul production building |
| Monster Fortress | 20100201 | Special | Monster stronghold |

### Battlefield Resource Objects

| Object Name | Code | Type | Description |
|-------------|------|------|-------------|
| BF Farm | 20700601 | Battlefield Resource | Battlefield food production |
| BF Forest | 20700602 | Battlefield Resource | Battlefield lumber production |
| BF Quarry | 20700603 | Battlefield Resource | Battlefield stone production |
| BF Gold Mine | 20700604 | Battlefield Resource | Battlefield gold production |
| BF Crystal Mine | 20700605 | Battlefield Resource | Battlefield crystal production |

### Special Buildings

| Object Name | Code | Type | Description |
|-------------|------|------|-------------|
| Kingdom | 20300101 | Special | Kingdom capital |
| Congress | 20400101 | Special | Government building |
| Shrine 1 | 20400201 | Special | Religious building |
| Shrine 2 | 20400202 | Special | Religious building |
| Shrine 3 | 20400203 | Special | Religious building |
| Alliance Center | 20600101 | Alliance | Alliance headquarters |
| Alliance Tower | 20600102 | Alliance | Alliance defensive structure |
| Outpost | 20600103 | Alliance | Alliance outpost |

### Gates and Fortresses

| Object Name | Code | Type | Description |
|-------------|------|------|-------------|
| Gate 1 | 20700101 | Gate | Transportation gate |
| Gate 2 | 20700102 | Gate | Transportation gate |
| Gate 3 | 20700103 | Gate | Transportation gate |
| Gate 4 | 20700104 | Gate | Transportation gate |
| Gate 5 | 20700105 | Gate | Transportation gate |
| Fortress 1 | 20700201 | Fortress | Defensive fortress |
| Fortress 2 | 20700202 | Fortress | Defensive fortress |
| Ancient Temple | 20700301 | Special | Ancient structure |

### Charms

| Object Name | Code | Type | Description |
|-------------|------|------|-------------|
| Charm Normal | 20500101 | Charm | Normal quality charm |
| Charm Magic | 20500102 | Charm | Magic quality charm |
| Charm Epic | 20500103 | Charm | Epic quality charm |
| Charm Legend | 20500104 | Charm | Legendary quality charm |

## Complete Monster Codes Reference

| Monster Name | Code | Type | Description |
|-------------|------|------|-------------|
| Orc | 20200101 | Monster | Basic monster unit |
| Skeleton | 20200102 | Monster | Undead monster unit |
| Golem | 20200103 | Monster | Stone construct monster |
| Treasure Goblin | 20200104 | Monster | Special loot monster |
| Deathkar | 20200201 | Boss | Elite boss monster |
| Green Dragon | 20200202 | Dragon | Green dragon boss |
| Red Dragon | 20200203 | Dragon | Red dragon boss |
| Gold Dragon | 20200204 | Dragon | Gold dragon boss |
| Magdar | 20200205 | Boss | Ultimate boss monster |

## Using Object and Monster Codes in Configuration

When configuring the `socf_thread` job, you can target any of the objects or monsters listed above by using their codes in the `targets` array. Here are some common targeting strategies:

### Resource Farming
```json
"targets": [
  {"code": 20100101, "level": []},  // All Farm levels
  {"code": 20100102, "level": [5, 6, 7]},  // Forest levels 5-7
  {"code": 20100105, "level": [1]}  // Only Crystal Mine level 1
]
```

### Monster Hunting
```json
"targets": [
  {"code": 20200101, "level": []},  // All Orc levels
  {"code": 20200102, "level": []},  // All Skeleton levels
  {"code": 20200104, "level": []}   // All Treasure Goblin levels
]
```

### Mixed Targeting
```json
"targets": [
  {"code": 20100105, "level": [1]},  // Crystal Mine level 1
  {"code": 20100106, "level": []},    // All Sealed Mine levels
  {"code": 20200101, "level": []},    // All Orc levels
  {"code": 20200104, "level": []}     // All Treasure Goblin levels
]
```

### Level Filtering
- **Empty array `[]`**: Target all levels of that object/monster
- **Specific levels `[1, 2, 3]`**: Target only the specified levels
- **Single level `[1]`**: Target only level 1

## Item Codes Reference

| Item Name | Code | Type |
|-----------|------|------|
| VIP 100 | 10101008 | VIP |
| Crystal 100 | 10101002 | Resource |
| Action Points 10 | 10101049 | Action Points |
| Action Points 20 | 10101050 | Action Points |
| Action Points 50 | 10101051 | Action Points |
| Action Points 100 | 10101052 | Action Points |

This architecture allows the bot to be both efficient (not constantly checking everything) and responsive (immediately handling time-sensitive tasks).
