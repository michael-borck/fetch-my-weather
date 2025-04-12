# Weather Mood Recommender

**Description:** Create a program that suggests activities based on the weather.

**Skills practiced:**
- String parsing
- Conditional logic
- Dictionary usage

**Sample code:**

```python
import fetch_my_weather
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
    weather_data = fetch_my_weather.get_weather(location=location, view_options="q")
    
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