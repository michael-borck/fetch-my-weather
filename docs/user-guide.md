# simple-weather User Guide

Welcome to `simple-weather`, a beginner-friendly Python package for accessing weather data! This guide will walk you through installation, basic usage, and advanced features.

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
pip install simple-weather
```

## Quick Start

Here's a basic example to get you started:

```python
import simple_weather

# Get current location weather (based on your IP address)
weather = simple_weather.get_weather()
print(weather)

# Get weather for a specific city
paris_weather = simple_weather.get_weather(location="Paris")
print(paris_weather)
```

## Core Features

### Getting Current Weather

When called without a location, `simple_weather` detects your location based on your IP address:

```python
import simple_weather

# Get weather for current location
current_weather = simple_weather.get_weather()
print(current_weather)
```

### Weather for a Specific Location

You can request weather for many types of locations:

```python
# City name
nyc_weather = simple_weather.get_weather(location="New York")

# Airport code
lax_weather = simple_weather.get_weather(location="LAX")

# Geographic coordinates (latitude,longitude)
paris_weather = simple_weather.get_weather(location="48.8567,2.3508")

# Special locations
mountain_weather = simple_weather.get_weather(location="~Mount Everest")
```

### Different Weather Views

The package supports different view options:

```python
# Full weather report (default)
full_weather = simple_weather.get_weather(location="London")

# Current weather only (no forecast)
current_only = simple_weather.get_weather(location="London", view_options="0")

# One-day forecast 
one_day = simple_weather.get_weather(location="London", view_options="1")

# Two-day forecast
two_day = simple_weather.get_weather(location="London", view_options="2")

# Narrow version (good for smaller terminals)
narrow = simple_weather.get_weather(location="London", view_options="n")

# Quiet version (no location in header)
quiet = simple_weather.get_weather(location="London", view_options="q")

# You can combine options
narrow_and_quiet = simple_weather.get_weather(location="London", view_options="nq")
narrow_quiet_one_day = simple_weather.get_weather(location="London", view_options="nq1")
```

### Changing Units

Choose between metric (default) and U.S. customary units:

```python
# Metric units (default)
metric = simple_weather.get_weather(location="Tokyo")

# US/Imperial units
imperial = simple_weather.get_weather(location="Tokyo", units="u")

# Metric with wind in m/s instead of km/h
metric_ms = simple_weather.get_weather(location="Tokyo", units="M")
```

### Language Support

Weather reports are available in many languages:

```python
# Spanish
spanish = simple_weather.get_weather(location="Madrid", lang="es")

# French
french = simple_weather.get_weather(location="Paris", lang="fr")

# German
german = simple_weather.get_weather(location="Berlin", lang="de")

# Japanese
japanese = simple_weather.get_weather(location="Tokyo", lang="ja")

# Russian
russian = simple_weather.get_weather(location="Moscow", lang="ru")

# Chinese (Simplified)
chinese = simple_weather.get_weather(location="Beijing", lang="zh-cn")
```

## Moon Phases

You can also get information about moon phases:

```python
# Current moon phase
moon = simple_weather.get_weather(is_moon=True)

# Moon phase for a specific date
future_moon = simple_weather.get_weather(is_moon=True, moon_date="2025-12-25")

# Moon phase with location hint (useful for timing)
us_moon = simple_weather.get_weather(is_moon=True, moon_location_hint=",+US")
paris_moon = simple_weather.get_weather(is_moon=True, moon_location_hint=",+Paris")
```

## Weather Images

Weather data can also be returned as PNG images:

```python
# Get weather as PNG image (returns bytes)
london_png = simple_weather.get_weather(location="London", is_png=True)

# Save the PNG to a file
with open("london_weather.png", "wb") as f:
    f.write(london_png)

# Get transparent PNG 
transparent_png = simple_weather.get_weather(
    location="London", 
    is_png=True, 
    png_options="t"
)

# Get PNG with padding
padded_png = simple_weather.get_weather(
    location="London", 
    is_png=True, 
    png_options="p"
)

# Combine PNG options
transparent_padded = simple_weather.get_weather(
    location="London", 
    is_png=True, 
    png_options="tp"
)
```

## Caching

To reduce unnecessary network requests, `simple_weather` caches responses for 10 minutes by default. You can control this behavior:

```python
import simple_weather

# Set cache duration to 30 minutes (1800 seconds)
simple_weather.set_cache_duration(1800)

# Disable caching completely
simple_weather.set_cache_duration(0)

# Clear the current cache
simple_weather.clear_cache()
```

## Error Handling

One of the key features of `simple_weather` is its beginner-friendly error handling. Instead of raising exceptions, it returns error messages as strings:

```python
import simple_weather

# Try to get weather for a location that might not exist
result = simple_weather.get_weather(location="NonExistentPlace12345")

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
simple_weather.set_user_agent("MyWeatherApp/1.0")
```

### Combining Multiple Options

You can combine different parameters to customize your request:

```python
# Get one-day forecast for Paris in French with US units in narrow format
paris_custom = simple_weather.get_weather(
    location="Paris",
    units="u",
    view_options="1n",
    lang="fr"
)
```

## Common Issues

### Network Problems

If you have connectivity issues, `simple_weather` will return an error message string:

```
Error: Could not connect to http://wttr.in/London. Check network connection.
```

In your code, always check if the result starts with "Error:" before trying to use it.

### Location Not Found

If a location cannot be found, you'll receive an error message. Try using more specific location information like coordinates or airport codes.

### Rate Limiting

The weather service may have rate limits. By default, `simple_weather` includes caching to reduce requests, but if you make too many unique requests too quickly, you might get error messages.

## Educational Notes

The `simple_weather` package is designed with education in mind:

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

---

We hope you enjoy using `simple_weather`! If you have any questions or suggestions, please feel free to open an issue on our GitHub repository.
