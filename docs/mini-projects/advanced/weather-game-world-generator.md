# Weather-based Game World Generator

**Description:** Create a game that generates different landscapes, challenges, and scenarios based on the real-world weather.

**Skills practiced:**
- Game development concepts
- Creative coding
- Environmental data integration
- ASCII art generation

**Sample code:**

```python
import fetch_my_weather
import random
import time
import os
import re
from datetime import datetime

class WeatherGame:
    def __init__(self):
        self.player = {
            "name": "Adventurer",
            "health": 100,
            "energy": 100,
            "inventory": ["map", "water bottle"],
            "position": (0, 0)
        }
        
        self.current_weather = None
        self.world_type = None
        self.enemies = []
        self.resources = []
        self.weather_effects = []
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_real_weather(self, location=""):
        """Get real-world weather and set game environment"""
        print("Connecting to weather service to generate your world...")
        
        # Use the JSON format and metadata feature for better error handling
        response = fetch_my_weather.get_weather(
            location=location, 
            format="json",  # Get structured data with Pydantic models
            with_metadata=True  # Get metadata about the response
        )
        
        # Extract data and metadata
        metadata = response.metadata
        weather_data = response.data
        
        if metadata.is_mock:
            if metadata.error_message:
                print(f"Note: Using mock data (Error: {metadata.error_message})")
            else:
                print("Note: Using mock data")
        
        # Extract game-relevant weather information from the structured data
        if weather_data.current_condition:
            current = weather_data.current_condition[0]
            
            # Get the weather condition
            condition = "clear"
            if current.weatherDesc and current.weatherDesc[0].value:
                weather_desc = current.weatherDesc[0].value.lower()
                if "rain" in weather_desc or "shower" in weather_desc:
                    condition = "rainy"
                elif "snow" in weather_desc or "blizzard" in weather_desc:
                    condition = "snowy"
                elif "cloud" in weather_desc or "overcast" in weather_desc:
                    condition = "cloudy"
                elif "fog" in weather_desc or "mist" in weather_desc:
                    condition = "foggy"
                elif "storm" in weather_desc or "thunder" in weather_desc:
                    condition = "stormy"
            
            # Determine if it's day or night
            is_day = True
            if weather_data.weather and weather_data.weather[0].astronomy:
                # Get the first day's astronomy data
                astronomy = weather_data.weather[0].astronomy[0]
                # Use current time to compare with sunrise/sunset
                current_time = datetime.now().strftime("%H:%M")
                if hasattr(astronomy, "sunrise") and hasattr(astronomy, "sunset"):
                    # Simple comparison, assuming 24-hour format
                    if current_time < astronomy.sunrise or current_time > astronomy.sunset:
                        is_day = False
            
            # Create the weather data structure
            self.current_weather = {
                "temperature": int(current.temp_C) if current.temp_C else 20,
                "condition": condition,
                "wind_speed": int(current.windspeedKmph) if current.windspeedKmph else 5,
                "humidity": int(current.humidity) if current.humidity else 60,
                "is_day": is_day
            }
            
            print(f"Weather data received: {self.current_weather['condition']}, {self.current_weather['temperature']}°C")
            return True
        else:
            # Fallback to default weather if no current condition data
            self.current_weather = {
                "temperature": 20,
                "condition": "clear",
                "wind_speed": 5,
                "humidity": 60,
                "is_day": True
            }
            print("Using default weather settings.")
            return False
    
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
        
        print(f"\nGenerated world: {self.world_type.upper()}")
        print(f"Based on: {weather['condition']} weather, {weather['temperature']}°C")
        print(f"Special effects: {', '.join(self.weather_effects)}")
    
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
    
    def get_random_encounter(self):
        """Generate a random encounter based on the world"""
        encounter_type = random.choice(["enemy", "resource", "effect"])
        
        if encounter_type == "enemy":
            enemy = random.choice(self.enemies)
            strength = random.randint(10, 30)
            return {
                "type": "enemy",
                "name": enemy,
                "strength": strength,
                "message": f"You encounter a {enemy} with strength {strength}!"
            }
        
        elif encounter_type == "resource":
            resource = random.choice(self.resources)
            amount = random.randint(1, 5)
            return {
                "type": "resource",
                "name": resource,
                "amount": amount,
                "message": f"You found {amount} {resource}!"
            }
        
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
        print("\n" + "!" * 40)
        print(encounter["message"])
        
        if encounter["type"] == "enemy":
            print("Options: [F]ight, [R]un away")
            choice = input("> ").strip().lower()
            
            if choice == "f":
                damage = random.randint(5, encounter["strength"])
                self.player["health"] -= damage
                print(f"You fought the {encounter['name']} and took {damage} damage.")
                
                # Add item to inventory
                if random.random() < 0.3:  # 30% chance
                    loot = f"{encounter['name']} trophy"
                    self.player["inventory"].append(loot)
                    print(f"You collected: {loot}")
            else:
                energy_cost = random.randint(5, 15)
                self.player["energy"] -= energy_cost
                print(f"You ran away, using {energy_cost} energy.")
        
        elif encounter["type"] == "resource":
            print("Options: [C]ollect, [I]gnore")
            choice = input("> ").strip().lower()
            
            if choice == "c":
                energy_cost = random.randint(1, 5)
                self.player["energy"] -= energy_cost
                self.player["inventory"].append(f"{encounter['name']} x{encounter['amount']}")
                print(f"You collected {encounter['amount']} {encounter['name']}, using {energy_cost} energy.")
            else:
                print("You decided to ignore the resources.")
        
        elif encounter["type"] == "effect":
            print("A weather effect impacts you!")
            if "damage" in encounter["name"]:
                damage = random.randint(3, 10)
                self.player["health"] -= damage
                print(f"You took {damage} damage from {encounter['name']}.")
            elif "stamina" in encounter["name"] or "energy" in encounter["name"]:
                energy_cost = random.randint(5, 15)
                self.player["energy"] -= energy_cost
                print(f"You lost {energy_cost} energy from {encounter['name']}.")
            else:
                print(f"The {encounter['name']} effect will persist for {encounter['duration']} turns.")
    
    def display_player_status(self):
        """Display player status"""
        player = self.player
        print("\n" + "-" * 40)
        print(f"Player: {player['name']}")
        print(f"Health: {player['health']}/100")
        print(f"Energy: {player['energy']}/100")
        print("Inventory:")
        for item in player['inventory']:
            print(f"  - {item}")
        print("-" * 40)
    
    def play_game(self):
        """Main game loop"""
        self.clear_screen()
        print("=== Weather Adventure Game ===")
        print("Your world will be generated based on the current weather!")
        
        # Get player name
        self.player["name"] = input("Enter your character name: ") or "Adventurer"
        
        # Get location for weather
        location = input("Enter location for weather (or press Enter for current location): ")
        
        # Get real weather and generate world
        self.get_real_weather(location)
        self.generate_world()
        
        # Game loop
        turns = 1
        while self.player["health"] > 0 and self.player["energy"] > 0 and turns <= 10:
            self.clear_screen()
            print(f"\n=== Turn {turns} ===")
            
            # Display world
            print(f"You are in the {self.world_type}.")
            self.display_world()
            
            # Display player status
            self.display_player_status()
            
            # Generate random encounter
            encounter = self.get_random_encounter()
            self.handle_encounter(encounter)
            
            # Check if player is still alive
            if self.player["health"] <= 0:
                print("\nYou have been defeated! Game over.")
                break
            if self.player["energy"] <= 0:
                print("\nYou are exhausted and can't continue! Game over.")
                break
            
            # Next turn
            if turns < 10:
                print("\nPress Enter to continue to the next turn...")
                input()
            
            turns += 1
        
        # Game end
        if turns > 10 and self.player["health"] > 0 and self.player["energy"] > 0:
            print("\nCongratulations! You survived the adventure!")
            print(f"Final stats - Health: {self.player['health']}, Energy: {self.player['energy']}")
            print(f"Items collected: {len(self.player['inventory'])} items")

# Run the game
if __name__ == "__main__":
    game = WeatherGame()
    game.play_game()
```

**Extensions:**
- Add more complex game mechanics (combat system, crafting, etc.)
- Implement a graphical interface with pygame
- Add more detailed weather effects on gameplay
- Create a persistent world that evolves with the changing weather