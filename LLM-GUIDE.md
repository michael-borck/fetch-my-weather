# fetch-my-weather LLM Guide

This guide provides comprehensive information about the `fetch-my-weather` Python package for large language models (LLMs) to understand its functionality, architecture, and usage patterns. 

## Package Overview

`fetch-my-weather` is a beginner-friendly Python package for fetching weather data, designed primarily for educational purposes. The package acts as a wrapper around the [wttr.in](https://github.com/chubin/wttr.in) weather service, providing an easy-to-use API with built-in error handling and caching.

### Core Features

- Easy access to weather data from wttr.in
- Moon phase information
- Location-based weather (cities, airports, coordinates)
- Multiple language support
- Text and PNG output formats
- Built-in caching to reduce API requests
- Beginner-friendly error handling (no exceptions)
- Designed for teaching Python and API interactions

## Installation

The package can be installed via pip:

```python
pip install fetch-my-weather
```

## API Reference

### Main Function

The primary function users will interact with is `get_weather()`:

```python
fetch_my_weather.get_weather(
    location: str = "",
    units: str = "",
    view_options: str = "",
    lang: Optional[str] = None,
    is_png: bool = False,
    png_options: str = "",
    is_moon: bool = False,
    moon_date: Optional[str] = None,
    moon_location_hint: Optional[str] = None,
) -> Union[str, bytes]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `location` | str | Location identifier (city name, airport code, coordinates, etc.). Empty for current location. |
| `units` | str | Units system: `m` (metric, default), `u` (US/imperial), `M` (wind in m/s) |
| `view_options` | str | Display options: `0`-`3` (forecast days), `n` (narrow), `q` (quiet), etc. |
| `lang` | str | Language code (e.g., `en`, `fr`, `es`, `ru`, `zh-cn`) |
| `is_png` | bool | If `True`, return PNG image as bytes instead of text |
| `png_options` | str | PNG-specific options: `p` (padding), `t` (transparency), etc. |
| `is_moon` | bool | If `True`, show moon phase instead of weather |
| `moon_date` | str | Date for moon phase in `YYYY-MM-DD` format (with `is_moon=True`) |
| `moon_location_hint` | str | Location hint for moon phase (e.g., `,+US`, `,+Paris`) |

#### Return Value

- If successful and not PNG: Returns the weather report as a string.
- If successful and PNG: Returns the PNG image data as bytes.
- If an error occurs: Returns an error message string (starting with "Error:").

### Configuration Functions

```python
# Set cache duration in seconds (0 to disable)
fetch_my_weather.set_cache_duration(seconds: int) -> int

# Clear the current cache
fetch_my_weather.clear_cache() -> int

# Set a custom user agent string
fetch_my_weather.set_user_agent(user_agent: str) -> str
```

## Usage Examples

### Basic Usage

```python
import fetch_my_weather

# Get weather for current location (based on IP)
weather = fetch_my_weather.get_weather()
print(weather)

# Get weather for a specific city
paris_weather = fetch_my_weather.get_weather(location="Paris")
print(paris_weather)

# Get weather with compact view and metric units
berlin_weather = fetch_my_weather.get_weather(
    location="Berlin", view_options="0", units="m"
)
print(berlin_weather)
```

### Getting Moon Phase Data

```python
# Current moon phase
moon = fetch_my_weather.get_weather(is_moon=True)
print(moon)

# Moon phase for specific date
christmas_moon = fetch_my_weather.get_weather(is_moon=True, moon_date="2025-12-25")
print(christmas_moon)
```

### Getting PNG Weather Images

```python
# Weather as PNG (returns bytes)
london_png = fetch_my_weather.get_weather(location="London", is_png=True)

# Save PNG to file
with open("london_weather.png", "wb") as f:
    f.write(london_png)

# PNG with transparency
transparent_png = fetch_my_weather.get_weather(
    location="Tokyo", is_png=True, png_options="t"
)
```

### Caching Control

```python
# Set cache duration to 30 minutes
fetch_my_weather.set_cache_duration(1800)

# Disable caching
fetch_my_weather.set_cache_duration(0)

# Clear the cache
fetch_my_weather.clear_cache()
```

### Error Handling Pattern

```python
# fetch-my-weather never raises exceptions, it returns error messages as strings
result = fetch_my_weather.get_weather(location="NonExistentPlace12345")

# Check if result is an error message
if isinstance(result, str) and result.startswith("Error:"):
    print(f"Something went wrong: {result}")
else:
    print("Weather data:", result)
```

## Architecture Details

The package has a simple, flat architecture:

```
src/fetch_my_weather/
├── __init__.py      # Exports public API
└── core.py          # Core implementation
```

Data flow:
1. User calls `get_weather()` with parameters
2. Parameters are validated
3. URL is constructed using `_build_url()`
4. Cache is checked using `_get_from_cache()`
5. If data is not in cache, HTTP request is made
6. Response is processed
7. Response is stored in cache using `_add_to_cache()`
8. Data is returned to the user

The caching system uses a simple in-memory dictionary with URL keys and (timestamp, data) values.

## Common Use Cases

1. **Simple Weather Check**: Get current location weather
2. **Multi-City Weather Comparison**: Get weather for multiple cities and compare
3. **Weather Images**: Generate weather images for display
4. **Moon Phase Information**: Get current or future moon phases
5. **Weather in Different Languages**: Get weather information in various languages
6. **Educational Projects**: Using the package to teach API interactions and data processing

## Project Ideas

The package includes mini-projects of varying difficulty levels:

### Beginner Projects
- Personal Weather Dashboard
- Multi-City Weather Checker
- Weather Image Saver

### Intermediate Projects
- Weather Mood Recommender
- Weekly Weather Forecast Tracker
- Weather-based Wallpaper Changer

### Advanced Projects
- Weather Notification System
- Weather Data Logger and Analyzer
- Weather-Based Home Automation
- Weather-based Game World Generator

## Best Practices

1. **Check for Errors**: Always check if the result starts with "Error:" before using it
2. **Use Caching**: Leverage the built-in caching to avoid unnecessary requests
3. **Respect the Service**: Don't make too many requests to wttr.in
4. **Handle PNG Returns**: Remember that PNG requests return bytes, not strings
5. **Use Compact Views**: Use view_options="0" or "1" for smaller, more focused weather data

## Key Limitations

1. **In-memory Cache**: Cache is not persistent across program restarts
2. **Network Dependency**: Requires internet connection to fetch weather data
3. **Service Limitations**: Subject to wttr.in service availability and rate limits

## Acknowledgments

This package is a wrapper around the [wttr.in](https://github.com/chubin/wttr.in) service created by [Igor Chubin](https://github.com/chubin).