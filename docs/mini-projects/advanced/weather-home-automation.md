# Weather-Based Home Automation Controller

**Description:** Build a system that controls smart home devices based on weather conditions.

**Skills practiced:**
- Integration with smart home APIs
- Event-based programming
- Configuration management
- Scheduled tasks

**Concept code:**

```python
import fetch_my_weather
import json
import time
import requests
from datetime import datetime

# Note: This is conceptual code that would need to be adapted
# to work with your specific smart home setup (Philips Hue, SmartThings, etc.)

class WeatherHomeAutomation:
    def __init__(self, config_file="weather_home_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.last_check = None
        self.current_weather = None
    
    def load_config(self):
        """Load configuration or create default"""
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except:
            # Default configuration
            default_config = {
                "location": "",  # Empty for auto-detect
                "check_interval_minutes": 15,
                "smart_home_api": {
                    "type": "hue",  # hue, smartthings, etc.
                    "host": "192.168.1.100",
                    "api_key": "your_api_key_here",
                },
                "rules": [
                    {
                        "condition": "rain",
                        "actions": [
                            {"device": "window", "command": "close"},
                            {"device": "living_room_light", "command": "on", "brightness": 80}
                        ]
                    },
                    {
                        "condition": "temperature_below",
                        "value": 5,
                        "actions": [
                            {"device": "thermostat", "command": "set_temp", "temperature": 22}
                        ]
                    },
                    {
                        "condition": "temperature_above",
                        "value": 25,
                        "actions": [
                            {"device": "fan", "command": "on", "speed": "medium"}
                        ]
                    },
                    {
                        "condition": "sunny",
                        "actions": [
                            {"device": "blinds", "command": "close"}
                        ]
                    },
                    {
                        "condition": "wind_above",
                        "value": 40,
                        "actions": [
                            {"device": "window", "command": "close"},
                            {"device": "awning", "command": "retract"}
                        ]
                    }
                ]
            }
            
            # Save default config
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=2)
            
            return default_config
    
    def get_current_weather(self):
        """Get current weather data using structured JSON format with metadata"""
        location = self.config["location"]
        
        # Get weather using JSON format with metadata
        response = fetch_my_weather.get_weather(
            location=location,
            format="json",
            with_metadata=True
        )
        
        # Extract data and metadata
        metadata = response.metadata
        weather_data = response.data
        
        # Check if using mock data
        if metadata.is_mock:
            print(f"Note: Using mock weather data for home automation.")
            if metadata.error_message:
                print(f"(Reason: {metadata.error_message})")
        
        # Process the structured data
        if weather_data.current_condition:
            # Get current condition data
            current = weather_data.current_condition[0]
            
            # Extract temperature
            temperature = None
            if current.temp_C:
                temperature = int(current.temp_C)
                
            # Extract wind speed
            wind_speed = None
            if current.windspeedKmph:
                wind_speed = int(current.windspeedKmph)
                
            # Determine conditions
            conditions = []
            weather_desc = ""
            if current.weatherDesc and current.weatherDesc[0].value:
                weather_desc = current.weatherDesc[0].value.lower()
                
                # Identify conditions
                if any(term in weather_desc for term in ["rain", "shower", "drizzle"]):
                    conditions.append("rain")
                if any(term in weather_desc for term in ["snow", "blizzard", "sleet"]):
                    conditions.append("snow")
                if any(term in weather_desc for term in ["sunny", "clear"]):
                    conditions.append("sunny")
                if any(term in weather_desc for term in ["cloud", "overcast"]):
                    conditions.append("cloudy")
                if any(term in weather_desc for term in ["fog", "mist"]):
                    conditions.append("fog")
                if any(term in weather_desc for term in ["thunder", "lightning", "storm"]):
                    conditions.append("thunderstorm")
            
            # Create weather data structure
            structured_data = {
                "timestamp": datetime.now().isoformat(),
                "text": weather_desc,  # Store the description text
                "conditions": {
                    "temperature": temperature,
                    "wind_speed": wind_speed,
                    "conditions": conditions
                }
            }
            
            self.current_weather = structured_data
            return structured_data
        else:
            print("Error: No current condition data available")
            return None
    
    def check_rule(self, rule):
        """Check if a rule should be triggered based on current weather"""
        if not self.current_weather:
            return False
        
        conditions = self.current_weather["conditions"]
        
        # Check different rule types
        if rule["condition"] == "rain" and "rain" in conditions["conditions"]:
            return True
        elif rule["condition"] == "snow" and "snow" in conditions["conditions"]:
            return True
        elif rule["condition"] == "sunny" and "sunny" in conditions["conditions"]:
            return True
        elif rule["condition"] == "cloudy" and "cloudy" in conditions["conditions"]:
            return True
        elif rule["condition"] == "foggy" and "fog" in conditions["conditions"]:
            return True
        elif rule["condition"] == "temperature_below" and conditions["temperature"] is not None:
            return conditions["temperature"] < rule["value"]
        elif rule["condition"] == "temperature_above" and conditions["temperature"] is not None:
            return conditions["temperature"] > rule["value"]
        elif rule["condition"] == "wind_above" and conditions["wind_speed"] is not None:
            return conditions["wind_speed"] > rule["value"]
        
        return False
    
    def execute_action(self, action):
        """Execute a home automation action"""
        # This would need to be implemented for your specific smart home system
        print(f"Executing action: {action}")
        
        api_config = self.config["smart_home_api"]
        api_type = api_config["type"]
        
        # Example for Philips Hue
        if api_type == "hue":
            if action["command"] == "on":
                self.hue_set_light(action["device"], True, action.get("brightness", 100))
            elif action["command"] == "off":
                self.hue_set_light(action["device"], False)
        
        # Example for a generic API
        elif api_type == "generic":
            self.generic_api_call(action)
    
    def hue_set_light(self, light_id, on, brightness=None):
        """Example function to control Philips Hue lights"""
        api_config = self.config["smart_home_api"]
        
        # Construct URL for Hue API
        url = f"http://{api_config['host']}/api/{api_config['api_key']}/lights/{light_id}/state"
        
        # Prepare data
        data = {"on": on}
        if on and brightness is not None:
            data["bri"] = min(254, int(brightness * 2.54))  # Convert percentage to Hue brightness
        
        # Make API call
        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                print(f"Successfully set light {light_id} to {on}, brightness: {brightness}")
            else:
                print(f"Error setting light: {response.text}")
        except Exception as e:
            print(f"Error calling Hue API: {e}")
    
    def generic_api_call(self, action):
        """Example function for a generic API call"""
        # This is a placeholder that would need to be customized for your smart home system
        print(f"Would make API call for: {action}")
    
    def check_and_execute_rules(self):
        """Check all rules and execute actions for those that match"""
        if not self.current_weather:
            return False
        
        triggered_actions = []
        
        for rule in self.config["rules"]:
            if self.check_rule(rule):
                print(f"Rule triggered: {rule['condition']}")
                for action in rule["actions"]:
                    triggered_actions.append(action)
        
        # Execute all triggered actions
        for action in triggered_actions:
            self.execute_action(action)
        
        return len(triggered_actions) > 0
    
    def run_automation_loop(self):
        """Run the main automation loop"""
        check_interval = self.config["check_interval_minutes"] * 60
        
        print(f"Weather Home Automation started. Checking every {check_interval/60} minutes.")
        print("Press Ctrl+C to exit.")
        
        try:
            while True:
                print(f"\nChecking weather at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
                self.get_current_weather()
                
                if self.current_weather:
                    print(f"Current conditions: {self.current_weather['conditions']}")
                    actions_triggered = self.check_and_execute_rules()
                    
                    if not actions_triggered:
                        print("No actions triggered.")
                
                # Sleep until next check
                print(f"Next check in {check_interval/60} minutes.")
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\nWeather Home Automation stopped.")

# Run the automation system
if __name__ == "__main__":
    import re  # Required for regex in extract_conditions
    
    automation = WeatherHomeAutomation()
    automation.run_automation_loop()
```

**Note:** This project is conceptual and would need adaptation to work with specific smart home systems. It demonstrates the approach but doesn't include actual implementations for various smart home APIs.

**Extensions:**
- Add a web interface for configuration
- Implement specific integrations for popular smart home platforms
- Add machine learning to improve automation decisions based on past patterns