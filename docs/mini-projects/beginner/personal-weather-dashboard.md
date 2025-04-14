# Personal Weather Dashboard

**Description:** Create a simple program that shows the weather for your location when you start your computer.

**Skills practiced:**
- Basic function calls
- String formatting
- Printing to console

**Sample code:**

```python
import fetch_my_weather

def show_my_weather():
    # Get current location weather with JSON format and metadata
    response = fetch_my_weather.get_weather(
        format="json",  # Use structured JSON format
        with_metadata=True  # Get metadata about the response
    )
    
    # Extract data and metadata
    metadata = response.metadata
    weather_data = response.data
    
    # Print a nice header
    print("=" * 50)
    print("TODAY'S WEATHER")
    print("=" * 50)
    
    # Check if using mock data
    if metadata.is_mock:
        print("Note: Using mock weather data")
        if metadata.error_message:
            print(f"(Reason: {metadata.error_message})")
    
    # Print weather details using the Pydantic model
    if weather_data.nearest_area and weather_data.nearest_area[0].areaName:
        location = weather_data.nearest_area[0].areaName[0].value
        print(f"Location: {location}")
    
    if weather_data.current_condition:
        current = weather_data.current_condition[0]
        
        # Print temperature
        print(f"Temperature: {current.temp_C}°C / {current.temp_F}°F")
        
        # Print weather description
        if current.weatherDesc:
            print(f"Condition: {current.weatherDesc[0].value}")
        
        # Print other details
        print(f"Humidity: {current.humidity}%")
        print(f"Wind: {current.windspeedKmph} km/h, {current.winddir16Point}")
        print(f"Pressure: {current.pressure} mb")
    
    # Print forecast if available
    if weather_data.weather:
        print("\nForecast:")
        for day in weather_data.weather[:3]:  # Next 3 days
            print(f"  {day.date}: {day.mintempC}°C to {day.maxtempC}°C")
    
    print("=" * 50)
    print("Have a great day!")

if __name__ == "__main__":
    show_my_weather()
```

**Extensions:**
- Add a greeting based on the time of day ("Good morning!", etc.)
- Save to a file instead of printing