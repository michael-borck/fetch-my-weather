# fetch-my-weather User Guide

Welcome to `fetch-my-weather`, a beginner-friendly Python package for accessing weather data! This guide will walk you through installation, basic usage, and advanced features.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Features](#core-features)
   - [Getting Current Weather](#getting-current-weather)
   - [Weather for a Specific Location](#weather-for-a-specific-location)
   - [Different Weather Views](#different-weather-views)
   - [Changing Units](#changing-units)
   - [Language Support](#language-support)
   - [Data Formats](#data-formats)
4. [Moon Phases](#moon-phases)
5. [Weather Images](#weather-images)
6. [Working with JSON & Models](#working-with-json--models)
7. [Caching](#caching)
8. [Mock Mode](#mock-mode)
9. [Error Handling](#error-handling)
10. [Advanced Usage](#advanced-usage)
11. [Common Issues](#common-issues)
12. [Educational Notes](#educational-notes)

## Installation

Installing the package is simple using pip:

```bash
pip install fetch-my-weather
```

## Quick Start

Here's a basic example to get you started:

```python
import fetch_my_weather

# Get current location weather as a structured model (default)
weather = fetch_my_weather.get_weather()
print(f"Temperature: {weather.current_condition[0].temp_C}°C")
print(f"Condition: {weather.current_condition[0].weatherDesc[0].value}")

# Get weather for a specific city as plain text
paris_weather = fetch_my_weather.get_weather(location="Paris", format="text")
print(paris_weather)
```

## Core Features

### Getting Current Weather

When called without a location, `fetch_my_weather` detects your location based on your IP address:

```python
import fetch_my_weather

# Get weather for current location (returns a Pydantic model by default)
current_weather = fetch_my_weather.get_weather()

# Access structured data
temperature = current_weather.current_condition[0].temp_C
condition = current_weather.current_condition[0].weatherDesc[0].value
print(f"It's {condition} and {temperature}°C")
```

### Weather for a Specific Location

You can request weather for many types of locations:

```python
# City name
nyc_weather = fetch_my_weather.get_weather(location="New York")

# Airport code
lax_weather = fetch_my_weather.get_weather(location="LAX")

# Geographic coordinates (latitude,longitude)
paris_weather = fetch_my_weather.get_weather(location="48.8567,2.3508")

# Special locations
mountain_weather = fetch_my_weather.get_weather(location="~Mount Everest")
```

### Different Weather Views

The package supports different view options:

```python
# Full weather report (default)
full_weather = fetch_my_weather.get_weather(location="London")

# Current weather only (no forecast)
current_only = fetch_my_weather.get_weather(location="London", view_options="0")

# One-day forecast 
one_day = fetch_my_weather.get_weather(location="London", view_options="1")

# Two-day forecast
two_day = fetch_my_weather.get_weather(location="London", view_options="2")

# Narrow version (good for smaller terminals)
narrow = fetch_my_weather.get_weather(location="London", view_options="n")

# Quiet version (no location in header)
quiet = fetch_my_weather.get_weather(location="London", view_options="q")

# You can combine options
narrow_and_quiet = fetch_my_weather.get_weather(location="London", view_options="nq")
narrow_quiet_one_day = fetch_my_weather.get_weather(location="London", view_options="nq1")
```

### Changing Units

Choose between metric (default) and U.S. customary units:

```python
# Metric units (default)
metric = fetch_my_weather.get_weather(location="Tokyo")

# US/Imperial units
imperial = fetch_my_weather.get_weather(location="Tokyo", units="u")

# Metric with wind in m/s instead of km/h
metric_ms = fetch_my_weather.get_weather(location="Tokyo", units="M")
```

### Language Support

Weather reports are available in many languages:

```python
# Spanish
spanish = fetch_my_weather.get_weather(location="Madrid", lang="es")

# French
french = fetch_my_weather.get_weather(location="Paris", lang="fr")

# German
german = fetch_my_weather.get_weather(location="Berlin", lang="de")

# Japanese
japanese = fetch_my_weather.get_weather(location="Tokyo", lang="ja")

# Russian
russian = fetch_my_weather.get_weather(location="Moscow", lang="ru")

# Chinese (Simplified)
chinese = fetch_my_weather.get_weather(location="Beijing", lang="zh-cn")
```

### Data Formats

The package supports multiple data formats to suit different needs:

```python
# JSON format (default) - returns a Pydantic model for structured data access
json_weather = fetch_my_weather.get_weather(location="London")
# Access data with type safety and autocompletion
temp = json_weather.current_condition[0].temp_C 

# Raw JSON format - returns a Python dictionary
raw_weather = fetch_my_weather.get_weather(location="London", format="raw_json")
# Access data using dictionary syntax
temp = raw_weather["current_condition"][0]["temp_C"]
condition = raw_weather["current_condition"][0]["weatherDesc"][0]["value"]

# Text format - returns plain text with ASCII art (for direct display)
text_weather = fetch_my_weather.get_weather(location="Paris", format="text")
print(text_weather)

# PNG format - returns image bytes
png_weather = fetch_my_weather.get_weather(location="Tokyo", format="png")
with open("weather.png", "wb") as f:
    f.write(png_weather)
```

## Moon Phases

You can also get information about moon phases:

```python
# Current moon phase
moon = fetch_my_weather.get_weather(is_moon=True)

# Moon phase for a specific date
future_moon = fetch_my_weather.get_weather(is_moon=True, moon_date="2025-12-25")

# Moon phase with location hint (useful for timing)
us_moon = fetch_my_weather.get_weather(is_moon=True, moon_location_hint=",+US")
paris_moon = fetch_my_weather.get_weather(is_moon=True, moon_location_hint=",+Paris")
```

## Weather Images

Weather data can also be returned as PNG images:

```python
# Get weather as PNG image using format parameter (returns bytes)
london_png = fetch_my_weather.get_weather(location="London", format="png")

# Save the PNG to a file
with open("london_weather.png", "wb") as f:
    f.write(london_png)

# Get transparent PNG 
transparent_png = fetch_my_weather.get_weather(
    location="London", 
    format="png", 
    png_options="t"
)

# Get PNG with padding
padded_png = fetch_my_weather.get_weather(
    location="London", 
    format="png", 
    png_options="p"
)

# Combine PNG options
transparent_padded = fetch_my_weather.get_weather(
    location="London", 
    format="png", 
    png_options="tp"
)

# Legacy method (deprecated but still supported)
legacy_png = fetch_my_weather.get_weather(location="London", is_png=True)
```

## Working with JSON & Models

When using the default JSON format, the package returns data as Pydantic models that provide type safety and structure:

```python
from fetch_my_weather import WeatherResponse

# Get weather data as a model (this is the default)
weather = fetch_my_weather.get_weather(location="London")

# Using type hints for better IDE support
weather_typed: WeatherResponse = fetch_my_weather.get_weather(location="London")

# Access current conditions
current = weather.current_condition[0]
print(f"Temperature: {current.temp_C}°C")
print(f"Feels like: {current.FeelsLikeC}°C")
print(f"Condition: {current.weatherDesc[0].value}")
print(f"Humidity: {current.humidity}%")
print(f"Wind: {current.windspeedKmph} km/h, {current.winddir16Point}")

# Access location information
location = weather.nearest_area[0]
print(f"Location: {location.areaName[0].value}, {location.country[0].value}")
print(f"Region: {location.region[0].value}")
print(f"Coordinates: {location.latitude}, {location.longitude}")

# Access forecast data
for day in weather.weather:
    print(f"Date: {day.date}")
    print(f"Max/Min: {day.maxtempC}°C/{day.mintempC}°C")
    
    # Access astronomy data
    astronomy = day.astronomy[0]
    print(f"Sunrise: {astronomy.sunrise}, Sunset: {astronomy.sunset}")
    
    # Access hourly forecast (just first entry as example)
    hour = day.hourly[0]
    print(f"Time: {hour.time}, Temp: {hour.tempC}°C")
```

## Caching

To reduce unnecessary network requests, `fetch_my_weather` caches responses for 10 minutes by default. You can control this behavior:

```python
import fetch_my_weather

# Set cache duration to 30 minutes (1800 seconds)
fetch_my_weather.set_cache_duration(1800)

# Disable caching completely
fetch_my_weather.set_cache_duration(0)

# Clear the current cache
fetch_my_weather.clear_cache()
```

## Mock Mode

For development and testing without hitting API rate limits, the package includes a mock mode:

```python
import fetch_my_weather

# Enable mock mode globally
fetch_my_weather.set_mock_mode(True)

# Now all requests will use mock data instead of real API calls
mock_weather = fetch_my_weather.get_weather(location="London")
print(f"Temperature: {mock_weather.current_condition[0].temp_C}°C")

# Use mock mode for a single request
real_weather = fetch_my_weather.get_weather(location="Paris", use_mock=False)
mock_weather = fetch_my_weather.get_weather(location="Berlin", use_mock=True)

# Disable mock mode
fetch_my_weather.set_mock_mode(False)
```

Mock mode provides realistic sample data that matches the structure of real API responses, making it ideal for:

- Development without internet connection
- Avoiding rate limits during testing
- Creating reproducible examples
- Writing unit tests

## Error Handling

One of the key features of `fetch_my_weather` is its beginner-friendly error handling. Instead of raising exceptions, it returns error messages as strings:

```python
import fetch_my_weather

# Try to get weather for a location that might not exist
result = fetch_my_weather.get_weather(location="NonExistentPlace12345")

# Check if we got an error message
if isinstance(result, str) and result.startswith("Error:"):
    print(f"Oops! Something went wrong: {result}")
elif isinstance(result, fetch_my_weather.WeatherResponse):
    print(f"Weather data received for {result.nearest_area[0].areaName[0].value}")
else:
    print("Weather data received (non-JSON format)")
```

## Advanced Usage

### Setting a Custom User Agent

```python
# Set a custom user agent (helpful if you're building an app)
fetch_my_weather.set_user_agent("MyWeatherApp/1.0")
```

### Combining Multiple Options

You can combine different parameters to customize your request:

```python
# Get one-day forecast for Paris in French with US units in narrow format
paris_custom = fetch_my_weather.get_weather(
    location="Paris",
    units="u",
    view_options="1n",
    lang="fr"
)
```

## Common Issues

### Network Problems

If you have connectivity issues, `fetch_my_weather` will return an error message string:

```
Error: Could not connect to http://wttr.in/London. Check network connection.
```

In your code, always check if the result starts with "Error:" before trying to use it.

### Location Not Found

If a location cannot be found, you'll receive an error message. Try using more specific location information like coordinates or airport codes.

### Rate Limiting

The weather service may have rate limits. By default, `fetch_my_weather` includes caching to reduce requests, but if you make too many unique requests too quickly, you might get error messages.

## Educational Notes

The `fetch_my_weather` package is designed with education in mind:

1. **Simplicity Over Complexity**: The API is intentionally kept simple with a single main function.

2. **Readable Error Messages**: Errors are returned as readable strings rather than exceptions, making it easier for beginners.

3. **Built-in Caching**: The caching system demonstrates how to avoid unnecessary network requests.

4. **Example-Rich Documentation**: Each feature is demonstrated with clear examples.

5. **Minimal Dependencies**: The package only requires the `requests` library, keeping it lightweight.

This package is ideal for:
- Introducing students to working with APIs
- Teaching basic network request concepts
- Demonstrating data retrieval and display
- Learning about caching and performance optimization

## Mini-Projects

To help you get started with practical applications, we've included a collection of mini-projects in the `docs/mini-projects/` directory. These are organized by difficulty level:

### Beginner Projects
- **Personal Weather Dashboard**: Simple program showing weather for your location
- **Multi-City Weather Checker**: Compare weather across multiple cities
- **Weather Image Saver**: Save weather data as PNG images

### Intermediate Projects
- **Weather Mood Recommender**: Get activity suggestions based on current weather
- **Weekly Weather Forecast Tracker**: Track and compare forecasts with actual weather
- **Weather-based Wallpaper Changer**: Change your desktop wallpaper based on weather

### Advanced Projects
- **Weather Notification System**: Get alerts for specific weather conditions
- **Weather Data Logger and Analyzer**: Track and visualize weather data over time
- **Weather-Based Home Automation**: Control smart home devices based on weather
- **Weather-based Game World Generator**: Create games that adapt to real-world weather

Each project includes full code samples and instructions. They're perfect for learning or teaching Python with real-world applications.

---

We hope you enjoy using `fetch_my_weather`! If you have any questions or suggestions, please feel free to open an issue on our GitHub repository.
