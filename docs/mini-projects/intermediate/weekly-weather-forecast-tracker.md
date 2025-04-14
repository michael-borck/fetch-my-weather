# Weekly Weather Forecast Tracker

**Description:** Create a program that tracks and compares weather forecasts with actual weather.

**Skills practiced:**
- File I/O
- Data persistence
- Date/time handling
- Text parsing

**Sample code:**

```python
import fetch_my_weather
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
    
    # Get the weather forecast using JSON format with metadata
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
        print(f"Note: Using mock weather data. This may affect forecast accuracy.")
        if metadata.error_message:
            print(f"(Reason: {metadata.error_message})")
    
    # Record date and forecast
    today = datetime.now()
    
    # Check if forecast file exists, create it if not
    file_exists = os.path.isfile('weather_forecast.csv')
    
    with open('weather_forecast.csv', 'a', newline='') as csvfile:
        fieldnames = ['forecast_date', 'target_date', 'forecasted_temp', 'actual_temp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        # Get forecasted temperatures from structured data
        if weather_data.weather:
            for i, day in enumerate(weather_data.weather):
                if i == 0:  # Skip today
                    continue
                    
                if i > 3:  # Only look at next 3 days
                    break
                
                # Get the date from the forecast
                target_date_str = day.date
                
                # Get max temperature for the day
                if day.maxtempC:
                    temp = day.maxtempC
                    
                    writer.writerow({
                        'forecast_date': today.strftime('%Y-%m-%d'),
                        'target_date': target_date_str,
                        'forecasted_temp': temp,
                        'actual_temp': ''  # Will be filled in later
                    })
                    print(f"Recorded forecast for {target_date_str}: {temp}°C")
        else:
            print("No forecast data available")

def update_actual_temperatures():
    """Update recorded forecasts with actual temperatures"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get today's actual weather using JSON format with metadata
    response = fetch_my_weather.get_weather(
        format="json",
        with_metadata=True
    )
    
    # Extract data and metadata
    metadata = response.metadata
    weather_data = response.data
    
    # Check if using mock data
    if metadata.is_mock:
        print(f"Note: Using mock weather data for actual temperature.")
        if metadata.error_message:
            print(f"(Reason: {metadata.error_message})")
    
    # Get the current temperature from structured data
    actual_temp = None
    if weather_data.current_condition and weather_data.current_condition[0].temp_C:
        actual_temp = weather_data.current_condition[0].temp_C
        print(f"Current temperature: {actual_temp}°C")
    
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
        print("Could not get current temperature data")

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