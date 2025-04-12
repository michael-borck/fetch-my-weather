# simple-weather

A beginner-friendly Python package for fetching weather data, designed for educational use.

## Features

- 🌤️ Easy access to weather data from wttr.in
- 🌙 Moon phase information
- 🗺️ Location-based weather (cities, airports, coordinates)
- 🌍 Multiple language support
- 📊 Text and PNG output formats
- 🚀 Built-in caching to be nice to the wttr.in service
- 🛡️ Beginner-friendly error handling (no exceptions)
- 📚 Designed for teaching Python and API interactions

## Installation

```bash
pip install simple-weather
```

## Quick Start

```python
import simple_weather

# Get weather for your current location (based on IP)
current_weather = simple_weather.get_weather()
print(current_weather)

# Get weather for Berlin in metric units
berlin_weather = simple_weather.get_weather(location="Berlin", units="m")
print(berlin_weather)

# Get moon phase for a specific date
moon = simple_weather.get_weather(is_moon=True, moon_date="2025-07-04")
print(moon)
```

## Teaching Applications

simple-weather is designed as a teaching tool for:

- Introducing API interactions in a beginner-friendly way
- Demonstrating HTTP requests without exception handling complexity
- Teaching caching concepts
- Working with different data formats (text and binary/PNG)
- Understanding URL construction and query parameters
- Processing and displaying weather data in applications

### Mini-Projects

The package includes a collection of ready-to-use mini-projects in the `docs/mini-projects/` directory:

- **Beginner projects**: Weather dashboard, multi-city checker, image saver
- **Intermediate projects**: Weather-based recommendations, forecast tracking, wallpaper changer
- **Advanced projects**: Notification system, data analyzer, home automation, weather-based game

These projects provide practical examples and serve as great teaching resources or starting points for your own applications.

## Usage Guide

### Getting Weather Data

```python
import simple_weather

# Basic usage - current location
weather = simple_weather.get_weather()

# Specific location
nyc_weather = simple_weather.get_weather(location="New York")

# Airport code
lax_weather = simple_weather.get_weather(location="lax")

# Geographic coordinates
coord_weather = simple_weather.get_weather(location="48.8567,2.3508")

# Compact view
compact_weather = simple_weather.get_weather(view_options="0")

# Compact view + quiet (no city name in header)
compact_quiet = simple_weather.get_weather(view_options="0q")

# Units: metric (default), USCS (u), or wind in m/s (M)
us_units = simple_weather.get_weather(units="u")

# Different language
spanish = simple_weather.get_weather(lang="es")
```

### Getting Moon Phase Data

```python
import simple_weather

# Current moon phase
moon = simple_weather.get_weather(is_moon=True)

# Moon phase for specific date
christmas_moon = simple_weather.get_weather(is_moon=True, moon_date="2025-12-25")

# Moon with location hint (affects timing)
paris_moon = simple_weather.get_weather(is_moon=True, moon_location_hint=",+Paris")
```

### Getting PNG Weather Images

```python
import simple_weather

# Weather as PNG (returns bytes)
london_png = simple_weather.get_weather(location="London", is_png=True)

# Save PNG to file
with open("london_weather.png", "wb") as f:
    f.write(london_png)

# PNG with options (transparency)
transparent_png = simple_weather.get_weather(location="Tokyo", is_png=True, png_options="t")
```

### Configuration Settings

```python
import simple_weather

# Change cache duration (in seconds, 0 to disable)
simple_weather.set_cache_duration(1800)  # 30 minutes

# Clear the cache
simple_weather.clear_cache()

# Set a custom user agent
simple_weather.set_user_agent("My Weather App v1.0")
```

### Error Handling

```python
import simple_weather

# simple-weather never raises exceptions, it returns error messages as strings
result = simple_weather.get_weather(location="NonExistentPlace12345")

# Check if result is an error message
if isinstance(result, str) and result.startswith("Error:"):
    print(f"Something went wrong: {result}")
else:
    print("Weather data:", result)
```

## Complete Parameter Reference

The `get_weather()` function accepts these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `location` | str | Location identifier (city name, airport code, coordinates, etc.) |
| `units` | str | Units system: `m` (metric, default), `u` (US/imperial), `M` (wind in m/s) |
| `view_options` | str | Display options: `0`-`3` (forecast days), `n` (narrow), `q` (quiet), etc. |
| `lang` | str | Language code (e.g., `en`, `fr`, `es`, `ru`, `zh-cn`) |
| `is_png` | bool | If `True`, return PNG image as bytes instead of text |
| `png_options` | str | PNG-specific options: `p` (padding), `t` (transparency), etc. |
| `is_moon` | bool | If `True`, show moon phase instead of weather |
| `moon_date` | str | Date for moon phase in `YYYY-MM-DD` format (with `is_moon=True`) |
| `moon_location_hint` | str | Location hint for moon phase (e.g., `,+US`, `,+Paris`) |

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This package is a wrapper around the amazing [wttr.in](https://github.com/chubin/wttr.in) service created by [Igor Chubin](https://github.com/chubin). Please be respectful of the wttr.in service by not making too many requests.
