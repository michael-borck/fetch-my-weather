# Weather Data Logger and Analyzer

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