# Multi-City Weather Checker

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