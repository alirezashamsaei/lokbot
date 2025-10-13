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

## Object Codes Reference

| Object Name | Code | Type |
|-------------|------|------|
| Crystal Mine | 20100105 | Resource |
| Dragon Soul Cavern | 20100106 | Resource |
| Orc | 20200101 | Monster |
| Skeleton | 20200102 | Monster |
| Golem | 20200103 | Monster |
| Goblin | 20200104 | Monster |

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
