# Multi-City Weather Checker

**Description:** Create a program that compares the weather in multiple cities of your choice.

**Skills practiced:**
- Working with lists
- Loops
- Function calls with parameters

**Sample code:**

```python
import fetch_my_weather
import time

def check_multiple_cities(cities):
    print("Checking weather in multiple cities...\n")
    
    for city in cities:
        print(f"Weather in {city}:")
        
        # Get weather with metadata to handle errors gracefully
        response = fetch_my_weather.get_weather(
            location=city, 
            format="json",  # Use JSON format with Pydantic models
            with_metadata=True  # Get metadata about the response
        )
        
        # Response is now a ResponseWrapper with both data and metadata
        metadata = response.metadata
        data = response.data
        
        # Check if this is real or mock data
        if metadata.is_mock:
            print(f"Note: Using mock data for {city}")
            if metadata.error_message:
                print(f"(Error: {metadata.error_message})")
                
        # Display current weather information using the Pydantic model
        if data.current_condition:
            current = data.current_condition[0]
            if current.weatherDesc:
                condition = current.weatherDesc[0].value
            else:
                condition = "Unknown"
                
            print(f"Temperature: {current.temp_C}°C / {current.temp_F}°F")
            print(f"Condition: {condition}")
            print(f"Humidity: {current.humidity}%")
            print(f"Wind: {current.windspeedKmph} km/h, {current.winddir16Point}")
            
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