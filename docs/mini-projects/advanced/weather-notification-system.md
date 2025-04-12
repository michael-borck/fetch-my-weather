# Weather Notification System

**Description:** Create a program that sends notifications when specific weather conditions occur.

**Skills practiced:**
- Scheduled tasks
- Notifications
- Pattern matching
- Configuration management

**Sample code:**

```python
import fetch_my_weather
import time
import json
import os
from datetime import datetime

# For Windows notifications
try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    notification_system = "windows"
except ImportError:
    # For macOS notifications
    try:
        import subprocess
        def notify_mac(title, message):
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
        notification_system = "mac"
    except:
        # Fallback to console
        notification_system = "console"

def send_notification(title, message):
    """Send a notification using platform-specific methods"""
    print(f"NOTIFICATION: {title} - {message}")
    
    if notification_system == "windows":
        toaster.show_toast(title, message, duration=10)
    elif notification_system == "mac":
        notify_mac(title, message)
    # For other platforms, we already printed to console

def load_config():
    """Load configuration or create default"""
    config_file = "weather_alerts_config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except:
            print("Error loading config file, using defaults")
    
    # Default configuration
    default_config = {
        "location": "",  # Empty for auto-detect
        "check_interval_minutes": 60,
        "alerts": {
            "rain": True,
            "snow": True,
            "extreme_temp": True,
            "extreme_temp_threshold_high": 30,  # °C
            "extreme_temp_threshold_low": 0,    # °C
            "wind": True,
            "wind_threshold": 50  # km/h
        },
        "last_alerts": {}
    }
    
    # Save default config
    with open(config_file, "w") as f:
        json.dump(default_config, f, indent=2)
    
    return default_config

def save_config(config):
    """Save configuration"""
    with open("weather_alerts_config.json", "w") as f:
        json.dump(config, f, indent=2)

def extract_temperature(weather_text):
    """Extract temperature from weather text"""
    for line in weather_text.split('\n'):
        if '°C' in line:
            parts = line.split('°C')[0].split()
            if parts and parts[-1].replace('-', '').isdigit():
                return int(parts[-1])
    return None

def extract_wind_speed(weather_text):
    """Extract wind speed from weather text"""
    for line in weather_text.split('\n'):
        if 'km/h' in line:
            parts = line.split('km/h')[0].split()
            if parts and parts[-1].isdigit():
                return int(parts[-1])
    return None

def check_weather_alerts():
    """Check weather and send alerts if conditions match"""
    config = load_config()
    location = config["location"]
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get current weather
    weather = fetch_my_weather.get_weather(location=location, view_options="q")
    
    if isinstance(weather, str) and not weather.startswith("Error:"):
        alerts_triggered = []
        weather_lower = weather.lower()
        
        # Check for rain
        if config["alerts"]["rain"] and ("rain" in weather_lower or "shower" in weather_lower):
            if "rain" not in config["last_alerts"] or config["last_alerts"]["rain"] != today:
                alerts_triggered.append(("Rain Alert", "Rain is expected today. Don't forget your umbrella!"))
                config["last_alerts"]["rain"] = today
        
        # Check for snow
        if config["alerts"]["snow"] and ("snow" in weather_lower or "blizzard" in weather_lower):
            if "snow" not in config["last_alerts"] or config["last_alerts"]["snow"] != today:
                alerts_triggered.append(("Snow Alert", "Snow is expected today. Dress warmly!"))
                config["last_alerts"]["snow"] = today
        
        # Check for extreme temperatures
        if config["alerts"]["extreme_temp"]:
            temp = extract_temperature(weather)
            if temp is not None:
                if temp >= config["alerts"]["extreme_temp_threshold_high"]:
                    if "high_temp" not in config["last_alerts"] or config["last_alerts"]["high_temp"] != today:
                        alerts_triggered.append(("Heat Alert", f"High temperature of {temp}°C expected today. Stay hydrated!"))
                        config["last_alerts"]["high_temp"] = today
                elif temp <= config["alerts"]["extreme_temp_threshold_low"]:
                    if "low_temp" not in config["last_alerts"] or config["last_alerts"]["low_temp"] != today:
                        alerts_triggered.append(("Cold Alert", f"Low temperature of {temp}°C expected today. Dress warmly!"))
                        config["last_alerts"]["low_temp"] = today
        
        # Check for strong wind
        if config["alerts"]["wind"]:
            wind = extract_wind_speed(weather)
            if wind is not None and wind >= config["alerts"]["wind_threshold"]:
                if "wind" not in config["last_alerts"] or config["last_alerts"]["wind"] != today:
                    alerts_triggered.append(("Wind Alert", f"Strong winds of {wind} km/h expected today. Be careful outside!"))
                    config["last_alerts"]["wind"] = today
        
        # Send notifications for triggered alerts
        for title, message in alerts_triggered:
            send_notification(title, message)
        
        # Save updated config with last alerts
        save_config(config)
        
        return len(alerts_triggered) > 0
    else:
        print(f"Error getting weather: {weather}")
        return False

def weather_alert_service():
    """Run the weather alert service continuously"""
    config = load_config()
    check_interval_minutes = config["check_interval_minutes"]
    
    print(f"Weather Alert Service started. Checking every {check_interval_minutes} minutes.")
    print(f"Press Ctrl+C to exit.")
    
    try:
        while True:
            print(f"\nChecking weather alerts at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
            alerts_sent = check_weather_alerts()
            
            if not alerts_sent:
                print("No new alerts triggered.")
            
            # Update interval from config in case it was changed
            config = load_config()
            check_interval_minutes = config["check_interval_minutes"]
            
            # Sleep until next check
            print(f"Next check in {check_interval_minutes} minutes.")
            time.sleep(check_interval_minutes * 60)
    except KeyboardInterrupt:
        print("\nWeather Alert Service stopped.")

# Run the service
if __name__ == "__main__":
    weather_alert_service()
```

**Extensions:**
- Create a GUI for configuring alert settings
- Add support for email or SMS notifications
- Implement a machine learning model to predict when alerts might be needed