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
    # Get weather data using JSON format and metadata for better handling
    response = fetch_my_weather.get_weather(
        location=location, 
        format="json",
        with_metadata=True
    )
    
    # Extract data and metadata
    metadata = response.metadata
    weather_data = response.data
    
    # Check if using mock data and notify if there was an error
    if metadata.is_mock and metadata.error_message:
        print(f"Note: Using mock weather data. ({metadata.error_message})")
    
    # Get the current weather condition
    condition = "unknown"
    temperature = 0
    
    if weather_data.current_condition:
        current = weather_data.current_condition[0]
        
        # Get weather description if available
        weather_desc = ""
        if current.weatherDesc and current.weatherDesc[0].value:
            weather_desc = current.weatherDesc[0].value.lower()
            
        # Get temperature
        if current.temp_C:
            temperature = int(current.temp_C)
        
        # Determine condition based on description and temperature
        if "sunny" in weather_desc or "clear" in weather_desc:
            condition = "sunny"
        elif "rain" in weather_desc or "drizzle" in weather_desc or "shower" in weather_desc:
            condition = "rainy"
        elif "cloud" in weather_desc or "overcast" in weather_desc:
            condition = "cloudy"
        elif "snow" in weather_desc or "blizzard" in weather_desc:
            condition = "snowy"
        elif temperature <= 5:
            condition = "cold"
        elif temperature >= 30:
            condition = "hot"
        else:
            # Default to a condition based on temperature range
            if temperature < 10:
                condition = "cold"
            elif temperature > 25:
                condition = "hot"
            else:
                condition = random.choice(["sunny", "cloudy", "rainy"])
        
        # Get random activity for the condition
        if condition in activities:
            activity = random.choice(activities[condition])
            return f"Based on the {condition} weather ({temperature}°C), you could: {activity}"
        else:
            return "No specific recommendation for this weather."
    else:
        return "Could not get weather data to make recommendations."

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