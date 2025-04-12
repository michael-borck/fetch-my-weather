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
4. [Moon Phases](#moon-phases)
5. [Weather Images](#weather-images)
6. [Caching](#caching)
7. [Error Handling](#error-handling)
8. [Advanced Usage](#advanced-usage)
9. [Common Issues](#common-issues)
10. [Educational Notes](#educational-notes)

## Installation

Installing the package is simple using pip:

```bash
pip install fetch-my-weather
```

## Quick Start

Here's a basic example to get you started:

```python
import fetch_my_weather

# Get current location weather (based on your IP address)
weather = fetch_my_weather.get_weather()
print(weather)

# Get weather for a specific city
paris_weather = fetch_my_weather.get_weather(location="Paris")
print(paris_weather)
```

## Core Features

### Getting Current Weather

When called without a location, `fetch_my_weather` detects your location based on your IP address:

```python
import fetch_my_weather

# Get weather for current location
current_weather = fetch_my_weather.get_weather()
print(current_weather)
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
# Get weather as PNG image (returns bytes)
london_png = fetch_my_weather.get_weather(location="London", is_png=True)

# Save the PNG to a file
with open("london_weather.png", "wb") as f:
    f.write(london_png)

# Get transparent PNG 
transparent_png = fetch_my_weather.get_weather(
    location="London", 
    is_png=True, 
    png_options="t"
)

# Get PNG with padding
padded_png = fetch_my_weather.get_weather(
    location="London", 
    is_png=True, 
    png_options="p"
)

# Combine PNG options
transparent_padded = fetch_my_weather.get_weather(
    location="London", 
    is_png=True, 
    png_options="tp"
)
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

## Error Handling

One of the key features of `fetch_my_weather` is its beginner-friendly error handling. Instead of raising exceptions, it returns error messages as strings:

```python
import fetch_my_weather

# Try to get weather for a location that might not exist
result = fetch_my_weather.get_weather(location="NonExistentPlace12345")

# Check if we got an error message
if isinstance(result, str) and result.startswith("Error:"):
    print(f"Oops! Something went wrong: {result}")
else:
    print("Weather data:", result)
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
