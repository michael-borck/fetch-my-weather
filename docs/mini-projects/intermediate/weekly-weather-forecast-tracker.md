# Weekly Weather Forecast Tracker

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