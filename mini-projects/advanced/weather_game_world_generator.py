#!/usr/bin/env python3
"""
Weather Game World Generator

A text-based adventure game that generates worlds, encounters, and gameplay
based on real-world weather data from the simple-weather package.

This is an enhanced version of the example from the mini-projects documentation.
"""

import simple_weather
import random
import time
import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union

class Item:
    """Game item class with properties and effects"""
    def __init__(self, name: str, item_type: str, value: int, description: str):
        self.name = name
        self.type = item_type  # "weapon", "armor", "potion", "resource", "trophy"
        self.value = value
        self.description = description
    
    def __str__(self) -> str:
        return f"{self.name} ({self.value})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert item to dictionary for saving"""
        return {
            "name": self.name,
            "type": self.type,
            "value": self.value,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """Create item from dictionary data"""
        return cls(
            name=data["name"],
            item_type=data["type"],
            value=data["value"],
            description=data["description"]
        )

class Crafting:
    """Crafting system for creating items from resources"""
    def __init__(self):
        # Define crafting recipes: (result, {ingredient1: count1, ingredient2: count2})
        self.recipes = {
            "healing potion": {"berries": 2, "rare herbs": 1},
            "energy potion": {"glowing mushrooms": 2, "water lilies": 1},
            "wooden shield": {"wood": 3},
            "ice spear": {"ice crystals": 2, "wood": 1},
            "storm staff": {"charged crystals": 2, "rare metals": 1},
        }
    
    def get_available_recipes(self, inventory: List[Item]) -> List[Tuple[str, Dict[str, int]]]:
        """Returns recipes that can be crafted with current inventory"""
        # Count resources in inventory
        resources = {}
        for item in inventory:
            if item.type == "resource":
                name = item.name.split(" x")[0]  # Handle "item x3" format
                if name in resources:
                    resources[name] += 1
                else:
                    resources[name] = 1
        
        # Check which recipes can be crafted
        available = []
        for recipe_name, ingredients in self.recipes.items():
            can_craft = True
            for ingredient, count in ingredients.items():
                if ingredient not in resources or resources[ingredient] < count:
                    can_craft = False
                    break
            
            if can_craft:
                available.append((recipe_name, ingredients))
        
        return available
    
    def craft_item(self, recipe_name: str, inventory: List[Item]) -> Tuple[bool, Optional[Item], List[Item]]:
        """
        Attempts to craft an item from inventory resources
        Returns: (success, crafted_item, updated_inventory)
        """
        if recipe_name not in self.recipes:
            return False, None, inventory
        
        # Check if we have the ingredients
        ingredients = self.recipes[recipe_name]
        resources = {}
        for item in inventory:
            if item.type == "resource":
                name = item.name.split(" x")[0]  # Handle "item x3" format
                if name in resources:
                    resources[name] += 1
                else:
                    resources[name] = 1
        
        # Verify we have all ingredients
        for ingredient, count in ingredients.items():
            if ingredient not in resources or resources[ingredient] < count:
                return False, None, inventory
        
        # Remove ingredients from inventory
        updated_inventory = inventory.copy()
        for ingredient, count in ingredients.items():
            # Remove count items of this ingredient
            remaining = count
            i = 0
            while i < len(updated_inventory) and remaining > 0:
                item = updated_inventory[i]
                if item.type == "resource" and item.name.split(" x")[0] == ingredient:
                    updated_inventory.pop(i)
                    remaining -= 1
                else:
                    i += 1
        
        # Create the crafted item
        if recipe_name == "healing potion":
            item = Item("Healing Potion", "potion", 25, "Restores 25 health points")
        elif recipe_name == "energy potion":
            item = Item("Energy Potion", "potion", 25, "Restores 25 energy points")
        elif recipe_name == "wooden shield":
            item = Item("Wooden Shield", "armor", 15, "Reduces damage by 15%")
        elif recipe_name == "ice spear":
            item = Item("Ice Spear", "weapon", 20, "A weapon with 20 damage")
        elif recipe_name == "storm staff":
            item = Item("Storm Staff", "weapon", 35, "A powerful magical weapon with 35 damage")
        else:
            item = Item(recipe_name.title(), "item", 10, f"A crafted {recipe_name}")
        
        # Add crafted item to inventory
        updated_inventory.append(item)
        return True, item, updated_inventory

class WeatherGame:
    def __init__(self):
        self.player = {
            "name": "Adventurer",
            "health": 100,
            "max_health": 100,
            "energy": 100,
            "max_energy": 100,
            "inventory": [],
            "position": (0, 0),
            "weapon": None,
            "armor": None,
            "turns_survived": 0,
            "enemies_defeated": 0
        }
        
        # Initialize starting items
        self.player["inventory"] = [
            Item("Map", "tool", 0, "Shows your current location"),
            Item("Water Bottle", "potion", 10, "Restores a small amount of energy")
        ]
        
        self.current_weather = None
        self.world_type = None
        self.enemies = []
        self.resources = []
        self.weather_effects = []
        self.crafting = Crafting()
        self.map = {}  # Dictionary of {(x, y): location_description}
        self.directions = ["north", "east", "south", "west"]
        self.persistent_effects = []  # List of [effect_name, turns_remaining]
        self.game_data_file = "weather_game_save.json"
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_real_weather(self, location=""):
        """Get real-world weather and set game environment"""
        print("Connecting to weather service to generate your world...")
        
        weather_text = simple_weather.get_weather(location=location, view_options="q")
        
        if isinstance(weather_text, str) and not weather_text.startswith("Error:"):
            # Extract key weather information
            self.current_weather = self.parse_weather(weather_text)
            print(f"Weather data received: {self.current_weather['condition']}, {self.current_weather['temperature']}°C")
            return True
        else:
            print(f"Error getting weather: {weather_text}")
            # Use default weather
            self.current_weather = {
                "temperature": 20,
                "condition": "clear",
                "wind_speed": 5,
                "humidity": 60,
                "is_day": True
            }
            print("Using default weather settings.")
            return False
    
    def parse_weather(self, weather_text):
        """Parse weather text into game-relevant data"""
        weather_lower = weather_text.lower()
        
        # Extract temperature
        temp_match = re.search(r'(\-?\d+)\s*°C', weather_text)
        temperature = int(temp_match.group(1)) if temp_match else 20
        
        # Extract wind speed
        wind_match = re.search(r'(\d+)\s*km/h', weather_text)
        wind_speed = int(wind_match.group(1)) if wind_match else 5
        
        # Extract humidity
        humidity_match = re.search(r'humidity\D+(\d+)', weather_lower)
        humidity = int(humidity_match.group(1)) if humidity_match else 60
        
        # Determine time of day
        is_day = True
        if "night" in weather_lower or "evening" in weather_lower:
            is_day = False
        
        # Determine condition
        condition = "clear"
        if "rain" in weather_lower or "shower" in weather_lower:
            condition = "rainy"
        elif "snow" in weather_lower or "blizzard" in weather_lower:
            condition = "snowy"
        elif "cloud" in weather_lower or "overcast" in weather_lower:
            condition = "cloudy"
        elif "fog" in weather_lower or "mist" in weather_lower:
            condition = "foggy"
        elif "storm" in weather_lower or "thunder" in weather_lower:
            condition = "stormy"
        
        return {
            "temperature": temperature,
            "condition": condition,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "is_day": is_day
        }
    
    def generate_world(self):
        """Generate game world based on weather"""
        weather = self.current_weather
        
        # Determine world type based on weather
        if weather["condition"] == "rainy":
            self.world_type = "swamp"
            self.enemies = ["frog warrior", "mud creature", "water elemental"]
            self.resources = ["mushrooms", "water lilies", "rare herbs"]
            self.weather_effects = ["reduced visibility", "slippery ground", "rising water"]
        
        elif weather["condition"] == "snowy":
            self.world_type = "tundra"
            self.enemies = ["frost wolf", "ice golem", "snow leopard"]
            self.resources = ["ice crystals", "winter berries", "frozen minerals"]
            self.weather_effects = ["cold damage", "limited stamina", "deep snow"]
        
        elif weather["condition"] == "cloudy":
            self.world_type = "highlands"
            self.enemies = ["mountain troll", "giant eagle", "rock creature"]
            self.resources = ["alpine flowers", "bird eggs", "precious stones"]
            self.weather_effects = ["occasional rain", "limited visibility", "gusty winds"]
        
        elif weather["condition"] == "foggy":
            self.world_type = "haunted forest"
            self.enemies = ["ghost", "shadow creature", "lost wanderer"]
            self.resources = ["glowing mushrooms", "spirit essence", "strange fruits"]
            self.weather_effects = ["disorientation", "invisibility", "whispers"]
        
        elif weather["condition"] == "stormy":
            self.world_type = "storm islands"
            self.enemies = ["lightning elemental", "storm drake", "cyclone spirit"]
            self.resources = ["charged crystals", "rare metals", "storm flowers"]
            self.weather_effects = ["lightning strikes", "heavy winds", "flooding"]
        
        else:  # clear/sunny
            self.world_type = "plains"
            self.enemies = ["wild boar", "bandit", "hawk"]
            self.resources = ["berries", "herbs", "wood"]
            self.weather_effects = ["heat exhaustion", "clear visibility", "dry terrain"]
        
        # Temperature modifiers
        if weather["temperature"] < 0:
            self.world_type = f"frozen {self.world_type}"
            self.weather_effects.append("freezing damage")
        elif weather["temperature"] > 30:
            self.world_type = f"scorching {self.world_type}"
            self.weather_effects.append("heat damage")
        
        # Day/night modifiers
        if not weather["is_day"]:
            self.world_type = f"nighttime {self.world_type}"
            self.enemies = ["night " + enemy for enemy in self.enemies]
            self.weather_effects.append("darkness")
        
        # Generate map: create a 5x5 grid with different locations based on world type
        self.generate_map()
        
        print(f"\nGenerated world: {self.world_type.upper()}")
        print(f"Based on: {weather['condition']} weather, {weather['temperature']}°C")
        print(f"Special effects: {', '.join(self.weather_effects)}")
    
    def generate_map(self):
        """Generate a map with different locations based on world type"""
        self.map = {}
        world_adjectives = [
            "misty", "dark", "bright", "shadowy", "quiet", 
            "noisy", "ancient", "forgotten", "hidden", "sacred",
            "dangerous", "peaceful", "mysterious", "enchanted", "cursed",
            "blessed", "wild", "tame", "desolate", "lush"
        ]
        
        # Locations based on world type
        if "swamp" in self.world_type:
            locations = [
                "marsh", "bog", "wetland", "quagmire", "mire",
                "mangrove", "bayou", "fen", "quicksand pit", "lily pond"
            ]
        elif "tundra" in self.world_type:
            locations = [
                "glacier", "ice field", "snow dune", "frozen lake", "frost valley",
                "ice cave", "crystal forest", "blizzard pass", "frozen waterfall", "snow plain"
            ]
        elif "highlands" in self.world_type:
            locations = [
                "mountain peak", "cliff edge", "rocky outcrop", "plateau", "mountain pass",
                "ridge", "valley", "ravine", "cave entrance", "waterfall"
            ]
        elif "haunted forest" in self.world_type:
            locations = [
                "dead grove", "twisted trees", "foggy clearing", "overgrown path", "ghostly glade",
                "whispering woods", "hollow tree", "ancient ruins", "forgotten shrine", "eerie stream"
            ]
        elif "storm" in self.world_type:
            locations = [
                "lightning field", "windy cliff", "rain-drenched valley", "thundering plateau", "flooded lowland",
                "stormy beach", "raging river", "battered coast", "cyclone zone", "tempest peak"
            ]
        else:  # plains
            locations = [
                "meadow", "grassland", "rolling hills", "stream", "small forest",
                "farm ruins", "lone tree", "wildflower field", "rocky outcrop", "village ruins"
            ]
        
        # Generate a 5x5 grid map
        for x in range(-2, 3):
            for y in range(-2, 3):
                # Special location at center
                if x == 0 and y == 0:
                    if random.random() < 0.7:
                        self.map[(x, y)] = f"safe haven (starting point)"
                    else:
                        self.map[(x, y)] = f"camp site (starting point)"
                else:
                    # Generate a random location description
                    adj = random.choice(world_adjectives)
                    loc = random.choice(locations)
                    self.map[(x, y)] = f"{adj} {loc}"
                    
                    # Don't reuse the same location and adjective
                    world_adjectives.remove(adj)
                    if not world_adjectives:  # Refill if empty
                        world_adjectives = ["misty", "dark", "bright", "shadowy", "quiet"]
                    locations.remove(loc)
                    if not locations:  # Refill if empty
                        locations = ["clearing", "hollow", "path", "grove", "ruins"]
    
    def display_world(self):
        """Display ASCII art for the current world"""
        if self.world_type is None:
            return
        
        # Simple ASCII art based on world type
        art = ""
        
        if "swamp" in self.world_type:
            art = """
            ~~~~~~~  ^^^^^  ~~~~~~~
             ~~ ~~  |.oo.|  ~~ ~~
            ~ ~ ~ ~ |..<.|~ ~ ~ ~
            ~~~~~~~~~~~~~~~~~~~~~~~~~
            """
        elif "tundra" in self.world_type:
            art = """
               /\\      /\\   *  *
              /  \\____/  \\    *  *
             /            \\  *  *
            /______________\\*******
            """
        elif "highlands" in self.world_type:
            art = """
                  /\\
                 /  \\      /\\
                /    \\    /  \\
               /      \\__/    \\
              /                \\
             /__________________\\
            """
        elif "haunted forest" in self.world_type:
            art = """
              (  )   (   )  )
                 ) (   )  (
                (  (   )    )
                   )  ) (
              |\\   (  |   )
              | )     \\|
              |/      ||
              /       |\\
             |        | )
             |        |/
            """
        elif "storm" in self.world_type:
            art = """
             \\    /    \\   /  ~~~~
              \\  /      \\ /  ~/~~~
            ~~~~~~~~~~~~~~~~~~~~~~~~
               ~~~~~~~~~~~~~~~~
                ~~~~~~~~~~
            """
        else:  # plains
            art = """
            
                        ^
            \\           |
             \\     ^    |    ^
              \\    |    |    |
               \\___|____|____|__
            """
        
        print(art)
    
    def display_map(self):
        """Display a visual map showing player position"""
        x, y = self.player["position"]
        print("\n=== MAP ===")
        for map_y in range(2, -3, -1):  # Top to bottom
            line = ""
            for map_x in range(-2, 3):  # Left to right
                if map_x == x and map_y == y:
                    line += "[@]"  # Player position
                elif (map_x, map_y) in self.map:
                    line += "[·]"  # Discovered location
                else:
                    line += "[ ]"  # Undiscovered location
            print(line)
        print("=========")
        print(f"You are at: {self.map.get(self.player['position'], 'unknown location')}")
    
    def get_random_encounter(self):
        """Generate a random encounter based on the world"""
        # Check for special locations that influence encounter chances
        loc_name = self.map.get(self.player["position"], "").lower()
        
        # Special cases for different locations
        if "camp" in loc_name or "haven" in loc_name or "starting point" in loc_name:
            # Higher chance of no encounter in safe areas
            encounter_type = random.choices(
                ["none", "enemy", "resource", "effect"], 
                weights=[0.5, 0.1, 0.3, 0.1]
            )[0]
        elif "ruins" in loc_name:
            # More enemies in ruins
            encounter_type = random.choices(
                ["enemy", "resource", "effect"], 
                weights=[0.6, 0.3, 0.1]
            )[0]
        elif any(res in loc_name for res in ["meadow", "grove", "forest", "field"]):
            # More resources in natural areas
            encounter_type = random.choices(
                ["enemy", "resource", "effect"], 
                weights=[0.3, 0.6, 0.1]
            )[0]
        else:
            # Normal probabilities
            encounter_type = random.choices(
                ["enemy", "resource", "effect"], 
                weights=[0.4, 0.4, 0.2]
            )[0]
        
        # No encounter
        if encounter_type == "none":
            return {
                "type": "none",
                "message": "You find a quiet moment to rest and plan your next move."
            }
        
        # Enemy encounter
        elif encounter_type == "enemy":
            enemy = random.choice(self.enemies)
            strength = random.randint(10, 30)
            enemy_health = strength * 2
            return {
                "type": "enemy",
                "name": enemy,
                "strength": strength,
                "health": enemy_health,
                "message": f"You encounter a {enemy} with strength {strength}!"
            }
        
        # Resource encounter
        elif encounter_type == "resource":
            resource = random.choice(self.resources)
            amount = random.randint(1, 5)
            return {
                "type": "resource",
                "name": resource,
                "amount": amount,
                "message": f"You found {amount} {resource}!"
            }
        
        # Weather effect encounter
        else:  # effect
            effect = random.choice(self.weather_effects)
            duration = random.randint(1, 3)
            return {
                "type": "effect",
                "name": effect,
                "duration": duration,
                "message": f"You experience {effect} for {duration} turns!"
            }
    
    def handle_encounter(self, encounter):
        """Handle a random encounter"""
        # No encounter
        if encounter["type"] == "none":
            print("\n" + "-" * 40)
            print(encounter["message"])
            
            # Small chance to heal or recover energy
            if random.random() < 0.3:
                heal = random.randint(5, 10)
                self.player["health"] = min(self.player["max_health"], self.player["health"] + heal)
                print(f"You recover {heal} health points while resting.")
            if random.random() < 0.3:
                energy = random.randint(5, 10)
                self.player["energy"] = min(self.player["max_energy"], self.player["energy"] + energy)
                print(f"You recover {energy} energy points while resting.")
            return
        
        # Regular encounters
        print("\n" + "!" * 40)
        print(encounter["message"])
        
        # Enemy encounter
        if encounter["type"] == "enemy":
            options = ["[F]ight", "[R]un away"]
            
            # Add use item option if player has potions
            has_usable_items = any(item.type == "potion" for item in self.player["inventory"])
            if has_usable_items:
                options.append("[U]se item")
            
            print("Options: " + ", ".join(options))
            choice = input("> ").strip().lower()
            
            # Use item
            if choice == "u" and has_usable_items:
                self.use_item()
                # After using item, still have to fight or run
                print("Options: [F]ight, [R]un away")
                choice = input("> ").strip().lower()
            
            # Fight
            if choice == "f":
                self.combat(encounter)
            # Run away
            else:
                escape_chance = 0.7  # Base escape chance
                
                # Apply modifiers
                if "slippery" in self.map.get(self.player["position"], ""):
                    escape_chance -= 0.2
                if any(effect[0] == "darkness" for effect in self.persistent_effects):
                    escape_chance -= 0.15
                
                # Try to escape
                if random.random() < escape_chance:
                    energy_cost = random.randint(5, 15)
                    self.player["energy"] -= energy_cost
                    print(f"You ran away, using {energy_cost} energy.")
                else:
                    print("You failed to escape! You have to fight.")
                    self.combat(encounter)
        
        # Resource encounter
        elif encounter["type"] == "resource":
            print("Options: [C]ollect, [I]gnore")
            choice = input("> ").strip().lower()
            
            if choice == "c":
                energy_cost = random.randint(1, 5)
                self.player["energy"] -= energy_cost
                
                # Create item and add to inventory
                resource_name = encounter["name"]
                amount = encounter["amount"]
                item = Item(f"{resource_name} x{amount}", "resource", amount, f"A valuable resource: {resource_name}")
                self.player["inventory"].append(item)
                
                print(f"You collected {amount} {resource_name}, using {energy_cost} energy.")
                
                # Sometimes find additional items
                if random.random() < 0.2:
                    bonus_item_name = random.choice(["small coin", "ancient artifact", "useful tool", "map fragment"])
                    bonus_item = Item(bonus_item_name, "treasure", random.randint(5, 20), f"A valuable {bonus_item_name}")
                    self.player["inventory"].append(bonus_item)
                    print(f"You also found a {bonus_item_name}!")
            else:
                print("You decided to ignore the resources.")
        
        # Weather effect encounter
        elif encounter["type"] == "effect":
            print("A weather effect impacts you!")
            effect_name = encounter["name"]
            duration = encounter["duration"]
            
            # Apply immediate effects
            if "damage" in effect_name:
                damage = random.randint(3, 10)
                self.player["health"] -= damage
                print(f"You took {damage} damage from {effect_name}.")
            elif "stamina" in effect_name or "energy" in effect_name:
                energy_cost = random.randint(5, 15)
                self.player["energy"] -= energy_cost
                print(f"You lost {energy_cost} energy from {effect_name}.")
            
            # Add persistent effect
            self.persistent_effects.append([effect_name, duration])
            print(f"The {effect_name} effect will persist for {duration} turns.")
    
    def combat(self, enemy_encounter):
        """Handle combat with an enemy"""
        enemy_name = enemy_encounter["name"]
        enemy_strength = enemy_encounter["strength"]
        enemy_health = enemy_encounter["health"]
        
        print(f"\nCombat with {enemy_name} begins!")
        print(f"Enemy health: {enemy_health}")
        
        # Combat loop
        round_num = 1
        while enemy_health > 0 and self.player["health"] > 0:
            print(f"\nRound {round_num}:")
            
            # Player's weapon bonus
            player_damage_bonus = 0
            if self.player["weapon"]:
                player_damage_bonus = self.player["weapon"].value
            
            # Player attacks
            hit_chance = 0.8  # Base hit chance
            
            # Apply modifiers from effects
            if any(eff[0] == "reduced visibility" for eff in self.persistent_effects):
                hit_chance -= 0.2
            if any(eff[0] == "darkness" for eff in self.persistent_effects):
                hit_chance -= 0.15
            
            if random.random() < hit_chance:
                damage = random.randint(5, 10) + player_damage_bonus
                enemy_health -= damage
                print(f"You hit the {enemy_name} for {damage} damage!")
            else:
                print(f"You missed the {enemy_name}!")
            
            # Check if enemy is defeated
            if enemy_health <= 0:
                print(f"You defeated the {enemy_name}!")
                self.player["enemies_defeated"] += 1
                
                # Chance to get a trophy or item
                if random.random() < 0.4:
                    item_type = random.choice(["trophy", "weapon", "armor", "potion"])
                    if item_type == "trophy":
                        item = Item(f"{enemy_name} trophy", "trophy", random.randint(1, 5), f"A trophy from defeating a {enemy_name}")
                    elif item_type == "weapon":
                        item = Item(f"{enemy_name} fang", "weapon", random.randint(5, 15), f"A weapon made from {enemy_name} parts")
                    elif item_type == "armor":
                        item = Item(f"{enemy_name} hide", "armor", random.randint(5, 15), f"Armor made from {enemy_name} hide")
                    else:  # potion
                        item = Item("Strange potion", "potion", random.randint(10, 20), "A mysterious potion with healing properties")
                    
                    self.player["inventory"].append(item)
                    print(f"You collected: {item.name}")
                
                # Chance to restore some health/energy
                if random.random() < 0.3:
                    heal = random.randint(5, 10)
                    self.player["health"] = min(self.player["max_health"], self.player["health"] + heal)
                    print(f"Victory energizes you! You recover {heal} health points.")
                
                break
            
            # Enemy attacks
            enemy_hit_chance = 0.7  # Base enemy hit chance
            
            # Apply modifiers
            if any(eff[0] == "darkness" for eff in self.persistent_effects):
                enemy_hit_chance += 0.1
            
            if random.random() < enemy_hit_chance:
                # Calculate damage with armor reduction
                raw_damage = random.randint(3, enemy_strength // 2)
                damage_reduction = 0
                if self.player["armor"]:
                    damage_reduction = self.player["armor"].value
                
                damage = max(1, int(raw_damage * (1 - damage_reduction/100)))
                self.player["health"] -= damage
                print(f"The {enemy_name} hits you for {damage} damage!")
            else:
                print(f"The {enemy_name} missed you!")
            
            # Show health status
            print(f"Your health: {self.player['health']}, Enemy health: {max(0, enemy_health)}")
            
            round_num += 1
            
            # Auto-use health potion if health is critical
            if self.player["health"] < 20:
                for i, item in enumerate(self.player["inventory"]):
                    if item.type == "potion" and "health" in item.name.lower():
                        print(f"\nAuto-using {item.name} because health is critical!")
                        self.player["health"] = min(self.player["max_health"], self.player["health"] + item.value)
                        print(f"Restored {item.value} health. Current health: {self.player['health']}")
                        self.player["inventory"].pop(i)
                        break
            
            # Optional pause between rounds
            input("Press Enter to continue combat...")
    
    def use_item(self):
        """Allow player to use an item from inventory"""
        # Find usable items
        usable_items = [(i, item) for i, item in enumerate(self.player["inventory"]) 
                        if item.type in ["potion", "food"]]
        
        if not usable_items:
            print("You don't have any usable items!")
            return
        
        # Show usable items
        print("\nUsable items:")
        for i, (idx, item) in enumerate(usable_items):
            print(f"  {i+1}. {item.name} - {item.description}")
        
        # Get choice
        try:
            choice = int(input("Enter item number to use (0 to cancel): ")) - 1
            if choice < 0:
                print("Cancelled item use.")
                return
            if choice >= len(usable_items):
                print("Invalid item number.")
                return
        except ValueError:
            print("Invalid input, expected a number.")
            return
        
        # Use the item
        item_idx, item = usable_items[choice]
        
        # Apply item effects
        if "health" in item.name.lower() or "healing" in item.name.lower():
            self.player["health"] = min(self.player["max_health"], self.player["health"] + item.value)
            print(f"You used {item.name} and restored {item.value} health.")
        elif "energy" in item.name.lower():
            self.player["energy"] = min(self.player["max_energy"], self.player["energy"] + item.value)
            print(f"You used {item.name} and restored {item.value} energy.")
        else:
            # Generic consumption
            self.player["health"] = min(self.player["max_health"], self.player["health"] + (item.value // 2))
            self.player["energy"] = min(self.player["max_energy"], self.player["energy"] + (item.value // 2))
            print(f"You used {item.name} and feel better.")
        
        # Remove the used item
        self.player["inventory"].pop(item_idx)
    
    def try_crafting(self):
        """Attempt to craft items from resources"""
        # Get available recipes
        available_recipes = self.crafting.get_available_recipes(self.player["inventory"])
        
        if not available_recipes:
            print("You don't have enough resources to craft anything!")
            return
        
        # Show available recipes
        print("\nAvailable recipes:")
        for i, (recipe_name, ingredients) in enumerate(available_recipes):
            ing_display = ", ".join([f"{count} {name}" for name, count in ingredients.items()])
            print(f"  {i+1}. {recipe_name.title()} - Requires: {ing_display}")
        
        # Get choice
        try:
            choice = int(input("Enter recipe number to craft (0 to cancel): ")) - 1
            if choice < 0:
                print("Cancelled crafting.")
                return
            if choice >= len(available_recipes):
                print("Invalid recipe number.")
                return
        except ValueError:
            print("Invalid input, expected a number.")
            return
        
        # Craft the item
        recipe_name = available_recipes[choice][0]
        success, item, updated_inventory = self.crafting.craft_item(recipe_name, self.player["inventory"])
        
        if success:
            self.player["inventory"] = updated_inventory
            print(f"You successfully crafted: {item.name} - {item.description}")
            
            # Auto-equip weapons and armor if better than current
            if item.type == "weapon" and (not self.player["weapon"] or item.value > self.player["weapon"].value):
                print(f"Equipped {item.name} as your weapon")
                self.player["weapon"] = item
            elif item.type == "armor" and (not self.player["armor"] or item.value > self.player["armor"].value):
                print(f"Equipped {item.name} as your armor")
                self.player["armor"] = item
        else:
            print("Crafting failed! Something went wrong.")
    
    def move_player(self):
        """Allow player to move on the map"""
        print("\nDirections you can go:")
        
        # Show available directions
        for i, direction in enumerate(self.directions):
            dx, dy = {
                "north": (0, 1),
                "east": (1, 0),
                "south": (0, -1),
                "west": (-1, 0)
            }[direction]
            
            # Calculate new position
            x, y = self.player["position"]
            new_x, new_y = x + dx, y + dy
            
            # Check if position is on the map
            if -2 <= new_x <= 2 and -2 <= new_y <= 2:
                loc_text = "unknown" if (new_x, new_y) not in self.map else self.map[(new_x, new_y)]
                print(f"  {i+1}. {direction.title()} - {loc_text}")
            else:
                print(f"  {i+1}. {direction.title()} - [You cannot go this way]")
        
        print("  0. Stay here")
        
        # Get choice
        try:
            choice = int(input("Choose direction (0-4): "))
            if choice == 0:
                print("You decide to stay where you are.")
                return False
            if choice < 1 or choice > 4:
                print("Invalid direction.")
                return False
        except ValueError:
            print("Invalid input, expected a number.")
            return False
        
        # Apply movement
        direction = self.directions[choice-1]
        dx, dy = {
            "north": (0, 1),
            "east": (1, 0),
            "south": (0, -1),
            "west": (-1, 0)
        }[direction]
        
        # Calculate new position
        x, y = self.player["position"]
        new_x, new_y = x + dx, y + dy
        
        # Check if position is valid
        if -2 <= new_x <= 2 and -2 <= new_y <= 2:
            # Movement cost
            energy_cost = 5  # Base movement cost
            
            # Apply modifiers from terrain
            loc_text = self.map.get((new_x, new_y), "").lower()
            
            if any(t in loc_text for t in ["mountain", "cliff", "peak", "ridge"]):
                energy_cost += 5
            if any(t in loc_text for t in ["marsh", "bog", "swamp", "quicksand"]):
                energy_cost += 3
            if any(ef[0] == "deep snow" for ef in self.persistent_effects):
                energy_cost += 3
            if any(ef[0] == "slippery ground" for ef in self.persistent_effects):
                energy_cost += 2
            
            # Apply movement
            self.player["energy"] -= energy_cost
            self.player["position"] = (new_x, new_y)
            print(f"You moved {direction} to {self.map.get((new_x, new_y), 'an unknown location')}.")
            print(f"This movement cost you {energy_cost} energy.")
            return True
        else:
            print("You cannot go that way - it's beyond the edge of the map.")
            return False
    
    def apply_persistent_effects(self):
        """Apply effects that persist across turns"""
        if not self.persistent_effects:
            return
        
        # Process each effect
        print("\nPersistent weather effects:")
        i = 0
        while i < len(self.persistent_effects):
            effect_name, turns_remaining = self.persistent_effects[i]
            
            # Apply effect
            if "damage" in effect_name:
                damage = random.randint(2, 7)
                self.player["health"] -= damage
                print(f"You take {damage} damage from {effect_name}.")
            elif "stamina" in effect_name or "energy" in effect_name:
                energy_loss = random.randint(2, 7)
                self.player["energy"] -= energy_loss
                print(f"You lose {energy_loss} energy from {effect_name}.")
            else:
                print(f"You are affected by: {effect_name}")
            
            # Reduce duration
            self.persistent_effects[i][1] -= 1
            
            # Remove expired effects
            if self.persistent_effects[i][1] <= 0:
                print(f"The {effect_name} effect has worn off.")
                self.persistent_effects.pop(i)
            else:
                print(f"  {turns_remaining-1} turns remaining.")
                i += 1
    
    def manage_inventory(self):
        """Display and manage inventory"""
        if not self.player["inventory"]:
            print("Your inventory is empty!")
            return
        
        print("\n=== INVENTORY ===")
        for i, item in enumerate(self.player["inventory"]):
            print(f"  {i+1}. {item.name} - {item.description}")
        
        print("\nEquipped items:")
        print(f"  Weapon: {self.player['weapon'].name if self.player['weapon'] else 'None'}")
        print(f"  Armor: {self.player['armor'].name if self.player['armor'] else 'None'}")
        
        print("\nInventory options:")
        print("  1. Use an item")
        print("  2. Examine an item")
        print("  3. Drop an item")
        print("  4. Equip weapon/armor")
        print("  0. Back to game")
        
        try:
            choice = int(input("Choose option (0-4): "))
            
            if choice == 1:
                self.use_item()
            elif choice == 2:
                # Examine item
                item_idx = int(input("Enter item number to examine: ")) - 1
                if 0 <= item_idx < len(self.player["inventory"]):
                    item = self.player["inventory"][item_idx]
                    print(f"\nExamining: {item.name}")
                    print(f"Type: {item.type}")
                    print(f"Value: {item.value}")
                    print(f"Description: {item.description}")
                else:
                    print("Invalid item number.")
            elif choice == 3:
                # Drop item
                item_idx = int(input("Enter item number to drop: ")) - 1
                if 0 <= item_idx < len(self.player["inventory"]):
                    dropped = self.player["inventory"].pop(item_idx)
                    print(f"You dropped: {dropped.name}")
                    
                    # Handle dropping equipped items
                    if self.player["weapon"] and self.player["weapon"].name == dropped.name:
                        self.player["weapon"] = None
                        print("You unequipped your weapon.")
                    if self.player["armor"] and self.player["armor"].name == dropped.name:
                        self.player["armor"] = None
                        print("You unequipped your armor.")
                else:
                    print("Invalid item number.")
            elif choice == 4:
                # Equip item
                print("\nEquippable items:")
                equippables = [(i, item) for i, item in enumerate(self.player["inventory"]) 
                               if item.type in ["weapon", "armor"]]
                
                if not equippables:
                    print("You don't have any equippable items!")
                    return
                
                for i, (idx, item) in enumerate(equippables):
                    print(f"  {i+1}. {item.name} ({item.type}, value: {item.value}) - {item.description}")
                
                item_choice = int(input("Enter item number to equip (0 to cancel): ")) - 1
                if item_choice < 0:
                    return
                if item_choice >= len(equippables):
                    print("Invalid item number.")
                    return
                
                idx, item = equippables[item_choice]
                
                if item.type == "weapon":
                    self.player["weapon"] = item
                    print(f"Equipped {item.name} as your weapon.")
                elif item.type == "armor":
                    self.player["armor"] = item
                    print(f"Equipped {item.name} as your armor.")
        except ValueError:
            print("Invalid input, expected a number.")
    
    def display_player_status(self):
        """Display player status"""
        player = self.player
        print("\n" + "-" * 40)
        print(f"Player: {player['name']}")
        print(f"Health: {player['health']}/{player['max_health']}")
        print(f"Energy: {player['energy']}/{player['max_energy']}")
        print(f"Position: {self.map.get(player['position'], 'unknown')}")
        print(f"Weapon: {player['weapon'].name if player['weapon'] else 'None'}")
        print(f"Armor: {player['armor'].name if player['armor'] else 'None'}")
        print(f"Inventory: {len(player['inventory'])} items")
        print(f"Enemies defeated: {player['enemies_defeated']}")
        print(f"Turns survived: {player['turns_survived']}")
        print("-" * 40)
    
    def save_game(self):
        """Save game state to a file"""
        save_data = {
            "player_name": self.player["name"],
            "health": self.player["health"],
            "max_health": self.player["max_health"],
            "energy": self.player["energy"],
            "max_energy": self.player["max_energy"],
            "position": self.player["position"],
            "enemies_defeated": self.player["enemies_defeated"],
            "turns_survived": self.player["turns_survived"],
            "inventory": [item.to_dict() for item in self.player["inventory"]],
            "weapon": self.player["weapon"].to_dict() if self.player["weapon"] else None,
            "armor": self.player["armor"].to_dict() if self.player["armor"] else None,
            "world_type": self.world_type,
            "map": self.map,
            "current_weather": self.current_weather,
            "persistent_effects": self.persistent_effects,
            "saved_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            with open(self.game_data_file, "w") as f:
                json.dump(save_data, f, indent=2)
            print(f"Game saved successfully to {self.game_data_file}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self):
        """Load game state from a file"""
        if not os.path.exists(self.game_data_file):
            print("No saved game found.")
            return False
        
        try:
            with open(self.game_data_file, "r") as f:
                save_data = json.load(f)
            
            # Restore player data
            self.player["name"] = save_data["player_name"]
            self.player["health"] = save_data["health"]
            self.player["max_health"] = save_data["max_health"]
            self.player["energy"] = save_data["energy"]
            self.player["max_energy"] = save_data["max_energy"]
            self.player["position"] = tuple(save_data["position"])
            self.player["enemies_defeated"] = save_data["enemies_defeated"]
            self.player["turns_survived"] = save_data["turns_survived"]
            
            # Restore inventory
            self.player["inventory"] = [Item.from_dict(item_data) for item_data in save_data["inventory"]]
            
            # Restore equipped items
            self.player["weapon"] = Item.from_dict(save_data["weapon"]) if save_data["weapon"] else None
            self.player["armor"] = Item.from_dict(save_data["armor"]) if save_data["armor"] else None
            
            # Restore world data
            self.world_type = save_data["world_type"]
            self.map = {tuple(map(int, k.strip("()").split(","))): v for k, v in save_data["map"].items()}
            self.current_weather = save_data["current_weather"]
            self.persistent_effects = save_data["persistent_effects"]
            
            print(f"Game loaded successfully from {self.game_data_file}")
            print(f"Last saved: {save_data['saved_on']}")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def show_game_menu(self):
        """Display the game menu and handle choices"""
        print("\n=== GAME MENU ===")
        print("1. Return to game")
        print("2. Save game")
        print("3. Load game")
        print("4. Inventory")
        print("5. Crafting")
        print("6. Show map")
        print("7. Show player status")
        print("8. Quit game")
        
        try:
            choice = int(input("Choose option (1-8): "))
            
            if choice == 1:
                return True  # Continue
            elif choice == 2:
                self.save_game()
            elif choice == 3:
                self.load_game()
            elif choice == 4:
                self.manage_inventory()
            elif choice == 5:
                self.try_crafting()
            elif choice == 6:
                self.display_map()
            elif choice == 7:
                self.display_player_status()
            elif choice == 8:
                confirm = input("Are you sure you want to quit? (y/n): ").lower()
                if confirm == "y":
                    save_first = input("Save game before quitting? (y/n): ").lower()
                    if save_first == "y":
                        self.save_game()
                    print("Thanks for playing!")
                    return False  # Quit
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input, expected a number.")
        
        return True  # Continue game by default
    
    def play_game(self):
        """Main game loop"""
        self.clear_screen()
        print("==========================")
        print("=== Weather Adventure Game ===")
        print("==========================")
        print("Your world will be generated based on the current weather!")
        print("\nGame options:")
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        
        try:
            choice = int(input("Choose option (1-3): "))
            
            if choice == 1:
                # New game
                self.clear_screen()
                print("=== New Game ===")
                
                # Get player name
                self.player["name"] = input("Enter your character name: ") or "Adventurer"
                
                # Get location for weather
                location = input("Enter location for weather (or press Enter for current location): ")
                
                # Get real weather and generate world
                self.get_real_weather(location)
                self.generate_world()
            elif choice == 2:
                # Load game
                if not self.load_game():
                    print("Could not load game. Starting new game instead.")
                    print("Press Enter to continue...")
                    input()
                    return self.play_game()  # Restart
            elif choice == 3:
                # Quit
                print("Thanks for playing!")
                return
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
                return self.play_game()  # Restart
        except ValueError:
            print("Invalid input, expected a number.")
            input("Press Enter to continue...")
            return self.play_game()  # Restart
        
        # Main game loop
        turns = 1
        self.player["turns_survived"] = 0
        
        while self.player["health"] > 0 and self.player["energy"] > 0:
            self.clear_screen()
            print(f"\n=== Turn {turns} ===")
            
            # Apply persistent effects at the start of the turn
            self.apply_persistent_effects()
            
            # Check if player died from effects
            if self.player["health"] <= 0 or self.player["energy"] <= 0:
                break
            
            # Display world
            print(f"You are in the {self.world_type}.")
            print(f"Location: {self.map.get(self.player['position'], 'unknown')}")
            self.display_world()
            
            # Display player status
            self.display_player_status()
            
            # Show menu
            print("\nActions:")
            print("1. Explore this area")
            print("2. Move to another location")
            print("3. Check inventory")
            print("4. Try crafting")
            print("5. Rest (recover energy)")
            print("6. Game menu")
            
            try:
                action = int(input("Choose action (1-6): "))
                
                if action == 1:
                    # Explore and trigger encounter
                    encounter = self.get_random_encounter()
                    self.handle_encounter(encounter)
                elif action == 2:
                    # Move to another location
                    self.move_player()
                elif action == 3:
                    # Check inventory
                    self.manage_inventory()
                elif action == 4:
                    # Try crafting
                    self.try_crafting()
                elif action == 5:
                    # Rest to recover energy
                    energy_gain = random.randint(10, 20)
                    self.player["energy"] = min(self.player["max_energy"], self.player["energy"] + energy_gain)
                    print(f"You take a short rest and recover {energy_gain} energy.")
                    
                    # Small chance of random encounter while resting
                    if random.random() < 0.3:
                        print("But your rest is interrupted!")
                        encounter = self.get_random_encounter()
                        self.handle_encounter(encounter)
                elif action == 6:
                    # Game menu
                    if not self.show_game_menu():
                        return  # Quit game
                else:
                    print("Invalid action. Please try again.")
            except ValueError:
                print("Invalid input, expected a number.")
            
            # Check if player is still alive
            if self.player["health"] <= 0:
                print("\nYou have been defeated! Game over.")
                break
            if self.player["energy"] <= 0:
                print("\nYou are exhausted and can't continue! Game over.")
                break
            
            # Next turn
            print("\nPress Enter to continue to the next turn...")
            input()
            
            turns += 1
            self.player["turns_survived"] = turns
        
        # Game end
        print("\n=== Game Over ===")
        print(f"You survived for {self.player['turns_survived']} turns.")
        print(f"Enemies defeated: {self.player['enemies_defeated']}")
        print(f"Items collected: {len(self.player['inventory'])}")
        
        # Ask to play again
        if input("Play again? (y/n): ").lower() == "y":
            self.play_game()

# Run the game
if __name__ == "__main__":
    game = WeatherGame()
    game.play_game()