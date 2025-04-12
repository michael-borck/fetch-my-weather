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
    # Get current location weather
    weather = fetch_my_weather.get_weather(view_options="q")
    
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