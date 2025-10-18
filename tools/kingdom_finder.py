#!/usr/bin/env python3
"""
Kingdom Finder Tool

A tool to search the entire map continent for player kingdoms by name or alliance tag.
Usage: python -m tools.kingdom_finder "player_name_or_tag"
"""

import sys
import time
import json
import socketio
import gzip
import threading
from typing import List, Dict, Any, Optional

# Add parent directory to path to import lokbot modules
sys.path.insert(0, '/home/alrzsh/projcts/lok_bot')

from lokbot.farmer import LokFarmer
from lokbot.enum import OBJECT_CODE_KINGDOM
from lokbot import logger, project_root
from lokbot.client import LokBotApi
from lokbot import config


class KingdomFinder:
    def __init__(self, token: str, captcha_solver_config: dict):
        """Initialize the kingdom finder with authentication."""
        self.farmer = LokFarmer(token, captcha_solver_config)
        self.api = self.farmer.api
        self.token = token
        self.search_query = ""
        self.matches = []
        self.scanned_zones = set()
        self.total_zones = 4096  # 64x64 zones
        self.zones_per_run = 63  # 7 grace * 9 step = 63 zones per run
        
    def get_all_continent_zones(self) -> List[int]:
        """Get all zone IDs in the current continent (0-4095)."""
        return list(range(4096))
    
    def search_kingdoms(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Search for kingdoms matching the given query using the same approach as socf_thread.
        
        Args:
            search_query: Player name to search for (case-insensitive)
            
        Returns:
            List of matching kingdoms with their details
        """
        self.search_query = search_query.lower()
        self.matches = []
        
        logger.info(f"Starting kingdom search for player name: '{search_query}'")
        
        # Wait for any recent API calls to complete (same as socf_thread)
        while self.api.last_requested_at + 16 > time.time():
            logger.info(f'last requested at {self.api.last_requested_at}, waiting...')
            time.sleep(4)
        
        # Use the same approach as socf_thread - scan in expanding radius
        from_loc = self.farmer.kingdom_enter.get('kingdom').get('loc')
        
        # Start with small radius and expand
        for radius in range(1, 33):  # Max radius of 32 to cover entire continent
            logger.info(f"Scanning with radius {radius}")
            zones = self.farmer._get_nearest_zone_ng(from_loc[1], from_loc[2], radius)
            
            if not zones:
                continue
                
            try:
                self._scan_zones_socf_style(zones)
            except Exception as e:
                logger.error(f"Error scanning radius {radius}: {e}")
                continue
            
            # If we found matches and radius is large enough, we can stop
            if len(self.matches) > 0 and radius > 16:
                logger.info(f"Found {len(self.matches)} matches, stopping search")
                break
        
        logger.info(f"Search completed. Found {len(self.matches)} matches.")
        return self.matches
    
    def _scan_zones_socf_style(self, zones: List[int]):
        """Scan zones using the exact same approach as socf_thread."""
        if not zones:
            return
            
        try:
            # Use the exact same approach as socf_thread
            self.farmer.socf_entered = False
            self.farmer.socf_world_id = self.farmer.kingdom_enter.get('kingdom').get('worldId')
            url = self.farmer.kingdom_enter.get('networks').get('fields')[0]
            
            # Use same headers as the main bot
            ws_headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Origin': 'https://play.leagueofkingdoms.com',
                'Pragma': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
            }
            
            sio = socketio.Client(reconnection=False, logger=logger, engineio_logger=logger)
            
            @sio.on('/field/objects/v4')
            def on_field_objects(data):
                try:
                    packs = data.get('packs')
                    gzip_decompress = gzip.decompress(bytearray(packs))
                    data_decoded = self.api.b64xor_dec(gzip_decompress)
                    objects = data_decoded.get('objects', [])
                    
                    logger.debug(f'Collected {len(objects)} objects from zones')
                    
                    # Filter for kingdom objects
                    for obj in objects:
                        if obj.get('code') == OBJECT_CODE_KINGDOM:
                            occupied = obj.get('occupied')
                            if occupied:
                                self._process_kingdom_object(obj, occupied)
                    
                    self.farmer.field_object_processed = True
                except Exception as e:
                    logger.error(f"Error processing field objects: {e}")
                    self.farmer.field_object_processed = True
            
            @sio.on('/field/enter/v3')
            def on_field_enter(data):
                try:
                    data_decoded = self.api.b64xor_dec(data)
                    logger.debug("Entered field")
                    self.farmer.socf_world_id = data_decoded.get('loc')[0]
                    
                    # Follow exact same sequence as socf_thread
                    sio.emit('/zone/leave/list/v2', {'world': self.farmer.socf_world_id, 'zones': '[]'})
                    default_zones = '[0,64,1,65]'
                    sio.emit('/zone/enter/list/v4', self.api.b64xor_enc({'world': self.farmer.socf_world_id, 'zones': default_zones}))
                    sio.emit('/zone/leave/list/v2', {'world': self.farmer.socf_world_id, 'zones': default_zones})
                    
                    self.farmer.socf_entered = True
                except Exception as e:
                    logger.error(f"Error in field enter: {e}")
                    self.farmer.socf_entered = True
            
            # Connect exactly like socf_thread
            sio.connect(f'{url}?token={self.token}', transports=["websocket"], headers=ws_headers)
            sio.emit('/field/enter/v3', self.api.b64xor_enc({'token': self.token}))
            
            # Wait for field entry
            while not self.farmer.socf_entered:
                time.sleep(0.1)
            
            # Process zones in batches like socf_thread
            step = 9
            grace = 7
            index = 0
            remaining_zones = zones.copy()
            
            while remaining_zones and index < grace:
                index += 1
                zone_ids = []
                for _ in range(step):
                    if not remaining_zones:
                        break
                    zone_ids.append(remaining_zones.pop(0))
                
                if not zone_ids:
                    break
                
                logger.debug(f'Entering zones: {zone_ids}')
                
                # Enter zones
                message = {'world': self.farmer.socf_world_id, 'zones': json.dumps(zone_ids, separators=(',', ':'))}
                encoded_message = self.api.b64xor_enc(message)
                sio.emit('/zone/enter/list/v4', encoded_message)
                
                # Wait for processing
                self.farmer.field_object_processed = False
                while not self.farmer.field_object_processed:
                    time.sleep(0.1)
                
                # Leave zones
                sio.emit('/zone/leave/list/v2', message)
            
            sio.disconnect()
            
        except Exception as e:
            logger.error(f"Error scanning zones: {e}")
    
    def _process_kingdom_object(self, obj: Dict[str, Any], occupied: Dict[str, Any]):
        """Process a kingdom object and check if it matches our search."""
        try:
            player_name = occupied.get('name', '').lower()
            loc = obj.get('loc', [])
            
            # Check if player name matches
            if self.search_query in player_name:
                
                match = {
                    'player_name': occupied.get('name', 'Unknown'),
                    'alliance_tag': occupied.get('allianceTag', 'No Alliance'),
                    'coordinates': {
                        'world': loc[0] if len(loc) > 0 else 'Unknown',
                        'x': loc[1] if len(loc) > 1 else 'Unknown', 
                        'y': loc[2] if len(loc) > 2 else 'Unknown'
                    },
                    'alliance_id': occupied.get('allianceId', ''),
                    'world_id': occupied.get('worldId', '')
                }
                
                self.matches.append(match)
                logger.info(f"Found match: {match['player_name']} ({match['alliance_tag']}) at ({match['coordinates']['x']}, {match['coordinates']['y']})")
                
        except Exception as e:
            logger.error(f"Error processing kingdom object: {e}")
    
    def display_results(self):
        """Display the search results in a formatted way."""
        if not self.matches:
            print(f"\n❌ No kingdoms found with player name matching '{self.search_query}'")
            return
        
        print(f"\n✅ Found {len(self.matches)} kingdom(s) with player name matching '{self.search_query}':")
        print("=" * 80)
        
        for i, match in enumerate(self.matches, 1):
            print(f"{i}. Player: {match['player_name']}")
            print(f"   Alliance: {match['alliance_tag']}")
            print(f"   Coordinates: ({match['coordinates']['x']}, {match['coordinates']['y']})")
            print(f"   World: {match['coordinates']['world']}")
            if match['alliance_id']:
                print(f"   Alliance ID: {match['alliance_id']}")
            print("-" * 40)


def main():
    """Main function to run the kingdom finder."""
    if len(sys.argv) != 2:
        print("Usage: python -m tools.kingdom_finder \"player_name\"")
        print("Example: python -m tools.kingdom_finder \"PlayerName\"")
        print("Example: python -m tools.kingdom_finder \"TestPlayer\"")
        sys.exit(1)
    
    search_query = sys.argv[1]
    
    try:
        # Load token from file
        token_path = project_root.joinpath('data/token')
        if not token_path.exists():
            print("❌ Error: Token file not found. Please run the main bot first to generate authentication.")
            sys.exit(1)
        
        token = token_path.read_text().strip()
        
        # Load config for captcha solver
        captcha_solver_config = config.get('captcha_solver', {})
        
        # Initialize and run the kingdom finder
        finder = KingdomFinder(token, captcha_solver_config)
        matches = finder.search_kingdoms(search_query)
        finder.display_results()
        
    except KeyboardInterrupt:
        print("\n⚠️ Search interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Kingdom finder error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
