# Mini-Projects with simple-weather

This document contains project ideas using the `simple-weather` package, ranging from beginner to intermediate level. These projects are designed to be educational, fun, and practical while teaching important programming concepts.

## Beginner Projects

### 1. Personal Weather Dashboard

**Description:** Create a simple program that shows the weather for your location when you start your computer.

**Skills practiced:**
- Basic function calls
- String formatting
- Printing to console

**Sample code:**

```python
import simple_weather

def show_my_weather():
    # Get current location weather
    weather = simple_weather.get_weather(view_options="q")
    
    # Print a nice header
    print("=" * 50)
    print("TODAY'S WEATHER")
    print("=" * 50)
    
    # Print the weather
    print(weather)
    
    print("=" * 50)
    print("Have a great day!")

if __name__ == "__main__":
    show_my_weather()
```

**Extensions:**
- Add a greeting based on the time of day ("Good morning!", etc.)
- Save to a file instead of printing

---

### 2. Multi-City Weather Checker

**Description:** Create a program that compares the weather in multiple cities of your choice.

**Skills practiced:**
- Working with lists
- Loops
- Function calls with parameters

**Sample code:**

```python
import simple_weather
import time

def check_multiple_cities(cities):
    print("Checking weather in multiple cities...\n")
    
    for city in cities:
        print(f"Weather in {city}:")
        weather = simple_weather.get_weather(location=city, view_options="0q")
        
        if isinstance(weather, str) and not weather.startswith("Error:"):
            print(weather)
        else:
            print(f"Could not get weather for {city}: {weather}")
            
        print("-" * 40)
        time.sleep(1)  # Be nice to the weather service
    
    print("Weather check complete!")

# List of cities to check
my_cities = ["New York", "London", "Tokyo", "Sydney", "Rio de Janeiro"]

# Run the function
check_multiple_cities(my_cities)
```

**Extensions:**
- Allow the user to input their own list of cities
- Sort the cities from warmest to coldest

---

### 3. Weather Image Saver

**Description:** Create a program that saves the current weather as a PNG image.

**Skills practiced:**
- Working with binary data
- File I/O
- Error handling

**Sample code:**

```python
import simple_weather
import os
from datetime import datetime

def save_weather_image(location, save_directory="weather_images"):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Get current date and time for the filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{save_directory}/{location.replace(' ', '_')}_{current_time}.png"
    
    # Get the weather as PNG
    print(f"Getting weather for {location}...")
    weather_png = simple_weather.get_weather(location=location, is_png=True)
    
    # Check if we got an error
    if not isinstance(weather_png, bytes):
        print(f"Error getting weather: {weather_png}")
        return False
    
    # Save the PNG to a file
    try:
        with open(filename, "wb") as f:
            f.write(weather_png)
        print(f"Saved weather image to {filename}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

# Save weather for New York
save_weather_image("New York")
```

**Extensions:**
- Add options for transparent or padded images
- Create a daily weather logger that saves an image every day

---

## Intermediate Projects

### 4. Weather Mood Recommender

**Description:** Create a program that suggests activities based on the weather.

**Skills practiced:**
- String parsing
- Conditional logic
- Dictionary usage

**Sample code:**

```python
import simple_weather
import random

# Activities based on weather conditions
activities = {
    "sunny": ["Go for a walk", "Have a picnic", "Visit the park", "Go cycling"],
    "rainy": ["Read a book", "Watch a movie", "Visit a museum", "Cook a new recipe"],
    "cloudy": ["Go shopping", "Visit friends", "Go to a café", "Take photographs"],
    "snowy": ["Build a snowman", "Go sledding", "Make hot chocolate", "Stay cozy inside"],
    "cold": ["Visit a museum", "Go to a coffee shop", "Try a new restaurant", "Go ice skating"],
    "hot": ["Go swimming", "Have ice cream", "Go to the beach", "Stay in air conditioning"]
}

def recommend_activity(location=""):
    # Get weather data
    weather_data = simple_weather.get_weather(location=location, view_options="q")
    
    if isinstance(weather_data, str) and not weather_data.startswith("Error:"):
        # Determine weather condition (this is a simplified approach)
        weather_lower = weather_data.lower()
        
        if "sunny" in weather_lower or "clear" in weather_lower:
            condition = "sunny"
        elif "rain" in weather_lower or "drizzle" in weather_lower or "shower" in weather_lower:
            condition = "rainy"
        elif "cloud" in weather_lower or "overcast" in weather_lower:
            condition = "cloudy"
        elif "snow" in weather_lower or "blizzard" in weather_lower:
            condition = "snowy"
        elif any(temp in weather_lower for temp in ["0 °c", "1 °c", "2 °c", "3 °c", "4 °c", "5 °c"]):
            condition = "cold"
        elif any(temp in weather_lower for temp in ["30 °c", "31 °c", "32 °c", "33 °c", "34 °c", "35 °c"]):
            condition = "hot"
        else:
            condition = random.choice(["sunny", "cloudy", "rainy"])
        
        # Get random activity for the condition
        if condition in activities:
            activity = random.choice(activities[condition])
            return f"Based on the {condition} weather, you could: {activity}"
        else:
            return "No specific recommendation for this weather."
    else:
        return f"Could not get weather: {weather_data}"

# Location to check
my_location = "London"

# Get and print the recommendation
print(f"Weather activity recommendation for {my_location}:")
recommendation = recommend_activity(my_location)
print(recommendation)
```

**Extensions:**
- Add more specific weather conditions and activities
- Allow users to add their own activities to the list
- Factor in the time of day for recommendations

---

### 5. Weekly Weather Forecast Tracker

**Description:** Create a program that tracks and compares weather forecasts with actual weather.

**Skills practiced:**
- File I/O
- Data persistence
- Date/time handling
- Text parsing

**Sample code:**

```python
import simple_weather
import csv
import os
from datetime import datetime, timedelta

def extract_temperature(weather_text):
    """Extract temperature from weather text (simple approach)"""
    for line in weather_text.split('\n'):
        if '°C' in line:
            parts = line.split('°C')[0].split()
            if parts and parts[-1].replace('-', '').isdigit():
                return int(parts[-1])
    return None

def record_forecast():
    """Record today's forecast for the next few days"""
    location = "London"  # Change to your location
    
    # Get the weather forecast
    forecast = simple_weather.get_weather(location=location)
    
    if isinstance(forecast, str) and not forecast.startswith("Error:"):
        # Record date and forecast
        today = datetime.now()
        
        # Check if forecast file exists, create it if not
        file_exists = os.path.isfile('weather_forecast.csv')
        
        with open('weather_forecast.csv', 'a', newline='') as csvfile:
            fieldnames = ['forecast_date', 'target_date', 'forecasted_temp', 'actual_temp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            # Extract forecasted temperatures (simplified approach)
            # In reality, you'd want to parse the forecast more carefully
            forecast_lines = forecast.split('\n')
            for i in range(1, 4):  # Look at next 3 days
                target_date = today + timedelta(days=i)
                target_date_str = target_date.strftime('%Y-%m-%d')
                
                # Get forecasted temperature (simplified)
                temp = extract_temperature(forecast)
                
                if temp is not None:
                    writer.writerow({
                        'forecast_date': today.strftime('%Y-%m-%d'),
                        'target_date': target_date_str,
                        'forecasted_temp': temp,
                        'actual_temp': ''  # Will be filled in later
                    })
                    print(f"Recorded forecast for {target_date_str}: {temp}°C")
    else:
        print(f"Could not get forecast: {forecast}")

def update_actual_temperatures():
    """Update recorded forecasts with actual temperatures"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get today's actual weather
    actual_weather = simple_weather.get_weather(view_options="0q")
    
    if isinstance(actual_weather, str) and not actual_weather.startswith("Error:"):
        # Extract actual temperature
        actual_temp = extract_temperature(actual_weather)
        
        if actual_temp is not None:
            # Read the existing CSV
            rows = []
            with open('weather_forecast.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Update rows where target_date is today and actual_temp is empty
                    if row['target_date'] == today and not row['actual_temp']:
                        row['actual_temp'] = actual_temp
                        print(f"Updated actual temperature for {today}: {actual_temp}°C")
                    rows.append(row)
            
            # Write the updated data back
            with open('weather_forecast.csv', 'w', newline='') as csvfile:
                fieldnames = ['forecast_date', 'target_date', 'forecasted_temp', 'actual_temp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
    else:
        print(f"Could not get actual weather: {actual_weather}")

def show_forecast_accuracy():
    """Show how accurate the forecasts have been"""
    if not os.path.isfile('weather_forecast.csv'):
        print("No forecast data available yet.")
        return
    
    # Read the CSV and calculate accuracy
    with open('weather_forecast.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        total_comparisons = 0
        total_difference = 0
        
        for row in reader:
            if row['actual_temp'] and row['forecasted_temp']:
                forecasted = int(row['forecasted_temp'])
                actual = int(row['actual_temp'])
                difference = abs(forecasted - actual)
                
                print(f"Date: {row['target_date']}")
                print(f"  Forecast made on: {row['forecast_date']}")
                print(f"  Forecasted temp: {forecasted}°C")
                print(f"  Actual temp: {actual}°C")
                print(f"  Difference: {difference}°C")
                print("-" * 30)
                
                total_comparisons += 1
                total_difference += difference
        
        if total_comparisons > 0:
            average_difference = total_difference / total_comparisons
            print(f"\nAverage forecast difference: {average_difference:.1f}°C over {total_comparisons} days")
        else:
            print("No completed forecast data available yet.")

# Run the functions
print("=== Weather Forecast Tracker ===")
print("1. Recording forecast...")
record_forecast()

print("\n2. Updating actual temperatures...")
update_actual_temperatures()

print("\n3. Forecast accuracy report:")
show_forecast_accuracy()
```

**Extensions:**
- Add more weather data points (precipitation, wind, etc.)
- Create visualization of forecast accuracy
- Set up an automated system to run daily

---

### 6. Weather-based Wallpaper Changer

**Description:** Create a program that changes your desktop wallpaper based on the current weather.

**Skills practiced:**
- System integration
- Image handling
- Conditional logic
- Scheduled tasks

**Sample code:**

```python
import simple_weather
import os
import platform
import ctypes
import subprocess
import tempfile
from datetime import datetime

def get_weather_condition():
    """Get the current weather condition"""
    weather = simple_weather.get_weather(view_options="0q")
    
    if isinstance(weather, str) and not weather.startswith("Error:"):
        # Simple weather condition detection (could be improved)
        weather_lower = weather.lower()
        
        if "rain" in weather_lower or "shower" in weather_lower:
            return "rainy"
        elif "snow" in weather_lower or "blizzard" in weather_lower:
            return "snowy"
        elif "cloud" in weather_lower or "overcast" in weather_lower:
            return "cloudy"
        elif "sunny" in weather_lower or "clear" in weather_lower:
            return "sunny"
        else:
            # Default to current weather image
            return "current"
    else:
        print(f"Error getting weather: {weather}")
        return None

def set_wallpaper(image_path):
    """Set the desktop wallpaper (platform specific)"""
    try:
        # Windows
        if platform.system() == "Windows":
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            return True
        # macOS
        elif platform.system() == "Darwin":
            script = f'''
            tell application "Finder"
                set desktop picture to POSIX file "{image_path}"
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            return True
        # Linux (assuming GNOME)
        elif platform.system() == "Linux":
            subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 
                           'picture-uri', f"file://{image_path}"], check=True)
            return True
        else:
            print(f"Unsupported platform: {platform.system()}")
            return False
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

def change_wallpaper_based_on_weather():
    """Change wallpaper based on current weather"""
    # Get current weather condition
    condition = get_weather_condition()
    
    if condition == "current":
        # Use current weather image as wallpaper
        temp_file = os.path.join(tempfile.gettempdir(), f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        # Get current weather as PNG with padding for better wallpaper fit
        weather_png = simple_weather.get_weather(is_png=True, png_options="p")
        
        if isinstance(weather_png, bytes):
            with open(temp_file, "wb") as f:
                f.write(weather_png)
            
            # Set as wallpaper
            if set_wallpaper(temp_file):
                print(f"Set current weather as wallpaper: {temp_file}")
                return True
    else:
        # In a real application, you would have custom wallpapers for each condition
        # For this example, we'll use the weather image
        print(f"Weather condition: {condition}")
        
        # Get weather image
        temp_file = os.path.join(tempfile.gettempdir(), f"weather_{condition}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        # Get current weather as PNG
        weather_png = simple_weather.get_weather(is_png=True, png_options="p")
        
        if isinstance(weather_png, bytes):
            with open(temp_file, "wb") as f:
                f.write(weather_png)
            
            # Set as wallpaper
            if set_wallpaper(temp_file):
                print(f"Set {condition} weather as wallpaper: {temp_file}")
                return True
    
    return False

# Run the function
print("Changing wallpaper based on weather...")
success = change_wallpaper_based_on_weather()
if success:
    print("Wallpaper changed successfully!")
else:
    print("Failed to change wallpaper.")
```

**Note:** This script attempts to work on Windows, macOS, and Linux, but platform-specific behavior might require adjustments.

**Extensions:**
- Add custom wallpapers for different weather conditions
- Create a scheduler that updates the wallpaper every few hours
- Add transition effects between wallpapers

---

## Intermediate/Advanced Projects

### 7. Weather Notification System

**Description:** Create a program that sends notifications when specific weather conditions occur.

**Skills practiced:**
- Scheduled tasks
- Notifications
- Pattern matching
- Configuration management

**Sample code:**

```python
import simple_weather
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
    weather = simple_weather.get_weather(location=location, view_options="q")
    
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

---

### 8. Weather Data Logger and Analyzer

**Description:** Create a system that logs weather data over time and generates reports with statistics and trends.

**Skills practiced:**
- Data logging
- File I/O with CSV
- Data analysis
- Visualization with matplotlib

**Sample code:**

```python
import simple_weather
import csv
import os
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import re

class WeatherLogger:
    def __init__(self, location="", log_file="weather_log.csv"):
        self.location = location
        self.log_file = log_file
        
        # Create log file with header if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'timestamp', 'location', 'temperature_c', 
                    'condition', 'humidity', 'wind_speed_kmh'
                ])
            print(f"Created new log file: {log_file}")
    
    def extract_temperature(self, weather_text):
        """Extract temperature from weather text"""
        match = re.search(r'(\-?\d+)\s*°C', weather_text)
        if match:
            return int(match.group(1))
        return None
    
    def extract_condition(self, weather_text):
        """Extract weather condition from text"""
        conditions = [
            "clear", "sunny", "partly cloudy", "cloudy", "overcast",
            "rain", "light rain", "heavy rain", "showers", "thunderstorm",
            "snow", "light snow", "heavy snow", "sleet", "hail", "fog", "mist"
        ]
        
        weather_lower = weather_text.lower()
        for condition in conditions:
            if condition in weather_lower:
                return condition
        return "unknown"
    
    def extract_humidity(self, weather_text):
        """Extract humidity percentage from text"""
        match = re.search(r'humidity\D+(\d+)', weather_text.lower())
        if match:
            return int(match.group(1))
        return None
    
    def extract_wind_speed(self, weather_text):
        """Extract wind speed from text"""
        match = re.search(r'(\d+)\s*km/h', weather_text)
        if match:
            return int(match.group(1))
        return None
    
    def log_current_weather(self):
        """Get current weather and log it to CSV"""
        # Get current weather
        weather = simple_weather.get_weather(location=self.location, view_options="q")
        
        if isinstance(weather, str) and not weather.startswith("Error:"):
            # Extract data points
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temperature = self.extract_temperature(weather)
            condition = self.extract_condition(weather)
            humidity = self.extract_humidity(weather)
            wind_speed = self.extract_wind_speed(weather)
            
            # Log to CSV
            with open(self.log_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    timestamp, self.location or "current", 
                    temperature, condition, humidity, wind_speed
                ])
            
            print(f"Logged weather data: {temperature}°C, {condition}, "
                  f"humidity: {humidity}%, wind: {wind_speed} km/h")
            return True
        else:
            print(f"Error getting weather: {weather}")
            return False
    
    def generate_daily_report(self, days=7):
        """Generate a report of the last X days of weather data"""
        if not os.path.exists(self.log_file):
            print(f"Log file not found: {self.log_file}")
            return False
        
        # Read the log file
        timestamps = []
        temperatures = []
        conditions = {}
        
        with open(self.log_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['temperature_c'] and row['timestamp']:
                    # Convert timestamp to datetime
                    timestamp = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                    
                    # Only include data from the last X days
                    if timestamp >= (datetime.now() - timedelta(days=days)):
                        timestamps.append(timestamp)
                        temperatures.append(float(row['temperature_c']))
                        
                        # Count conditions
                        condition = row['condition'] or "unknown"
                        if condition in conditions:
                            conditions[condition] += 1
                        else:
                            conditions[condition] = 1
        
        if not timestamps:
            print("No data available for the specified time period.")
            return False
        
        # Generate temperature chart
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, temperatures, marker='o', linestyle='-')
        plt.title(f"Temperature over the last {days} days")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the chart
        chart_file = f"temperature_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(chart_file)
        plt.close()
        
        # Generate condition pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(conditions.values(), labels=conditions.keys(), autopct='%1.1f%%')
        plt.title("Weather Conditions Distribution")
        plt.tight_layout()
        
        # Save the pie chart
        pie_file = f"conditions_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(pie_file)
        plt.close()
        
        # Print statistics
        avg_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        
        print("\n=== Weather Report ===")
        print(f"Period: Last {days} days")
        print(f"Data points: {len(temperatures)}")
        print(f"Average temperature: {avg_temp:.1f}°C")
        print(f"Maximum temperature: {max_temp}°C")
        print(f"Minimum temperature: {min_temp}°C")
        print("\nWeather conditions:")
        for condition, count in sorted(conditions.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(temperatures)) * 100
            print(f"  {condition}: {count} ({percentage:.1f}%)")
        
        print(f"\nCharts saved as {chart_file} and {pie_file}")
        return True

def log_weather_periodically(location="", interval_minutes=60, duration_hours=24):
    """Log weather at regular intervals for a specified duration"""
    logger = WeatherLogger(location)
    iterations = int((duration_hours * 60) / interval_minutes)
    
    print(f"Starting weather logging for {location or 'current location'}")
    print(f"Interval: {interval_minutes} minutes")
    print(f"Duration: {duration_hours} hours ({iterations} measurements)")
    print("Press Ctrl+C to stop logging early.")
    
    try:
        for i in range(iterations):
            print(f"\nLogging iteration {i+1}/{iterations}")
            logger.log_current_weather()
            
            if i < iterations - 1:  # Don't sleep after the last iteration
                print(f"Next log in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
        
        print("\nLogging complete. Generating report...")
        logger.generate_daily_report()
        
    except KeyboardInterrupt:
        print("\nLogging stopped early by user.")
        print("Generating report with data collected so far...")
        logger.generate_daily_report()

# Example usage
if __name__ == "__main__":
    location = input("Enter location (or press Enter for current location): ")
    interval = int(input("Enter logging interval in minutes (default: 60): ") or "60")
    duration = int(input("Enter logging duration in hours (default: 24): ") or "24")
    
    log_weather_periodically(location, interval, duration)
```

**Note:** This project requires matplotlib for visualization (`pip install matplotlib`).

**Extensions:**
- Add more sophisticated data analysis (trends, correlations)
- Create a web dashboard to display the data
- Implement prediction models based on historical data

---

## Advanced Projects

### 9. Weather-Based Home Automation Controller

**Description:** Build a system that controls smart home devices based on weather conditions.

**Skills practiced:**
- Integration with smart home APIs
- Event-based programming
- Configuration management
- Scheduled tasks

**Concept code:**

```python
import simple_weather
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
        """Get current weather data"""
        location = self.config["location"]
        weather_text = simple_weather.get_weather(location=location, view_options="q")
        
        if isinstance(weather_text, str) and not weather_text.startswith("Error:"):
            weather_data = {
                "timestamp": datetime.now().isoformat(),
                "text": weather_text,
                "conditions": self.extract_conditions(weather_text)
            }
            self.current_weather = weather_data
            return weather_data
        else:
            print(f"Error getting weather: {weather_text}")
            return None
    
    def extract_conditions(self, weather_text):
        """Extract conditions from weather text"""
        weather_lower = weather_text.lower()
        
        # Extract temperature
        temp_match = re.search(r'(\-?\d+)\s*°C', weather_text)
        temperature = int(temp_match.group(1)) if temp_match else None
        
        # Extract wind speed
        wind_match = re.search(r'(\d+)\s*km/h', weather_text)
        wind_speed = int(wind_match.group(1)) if wind_match else None
        
        # Determine conditions
        conditions = []
        
        if "rain" in weather_lower or "shower" in weather_lower:
            conditions.append("rain")
        if "snow" in weather_lower or "blizzard" in weather_lower:
            conditions.append("snow")
        if "sunny" in weather_lower or "clear" in weather_lower:
            conditions.append("sunny")
        if "cloud" in weather_lower or "overcast" in weather_lower:
            conditions.append("cloudy")
        if "fog" in weather_lower or "mist" in weather_lower:
            conditions.append("fog")
        if "thunder" in weather_lower or "lightning" in weather_lower:
            conditions.append("thunderstorm")
        
        return {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "conditions": conditions
        }
    
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

---

### 10. Weather-based Game World Generator

**Description:** Create a game that generates different landscapes, challenges, and scenarios based on the real-world weather.

**Skills practiced:**
- Game development concepts
- Creative coding
- Environmental data integration
- ASCII art generation

**Sample code:**

```python
import simple_weather
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