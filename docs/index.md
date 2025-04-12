# Simple Weather

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
pip install fetch-my-weather
```

## Quick Start

```python
import fetch_my_weather

# Get weather for your current location (based on IP)
current_weather = fetch_my_weather.get_weather()
print(current_weather)

# Get weather for Berlin in metric units
berlin_weather = fetch_my_weather.get_weather(location="Berlin", units="m")
print(berlin_weather)

# Get moon phase for a specific date
moon = fetch_my_weather.get_weather(is_moon=True, moon_date="2025-07-04")
print(moon)
```

## Navigation

- Check out the [User Guide](user-guide.md) for detailed usage instructions
- Explore the [Mini-Projects](mini-projects/README.md) for practical examples
- See the [Teaching Guide](teaching-guide.md) for educational applications
- Review the [Technical Documentation](technical-doc.md) for implementation details

## Contributors

This project is maintained by [Michael Borck](https://github.com/michael-borck) with contributions from various individuals. See the [AUTHORS file](AUTHORS.md) for a complete list of contributors.

## Acknowledgments

This package is a wrapper around the amazing [wttr.in](https://github.com/chubin/wttr.in) service created by [Igor Chubin](https://github.com/chubin). Please be respectful of the wttr.in service by not making too many requests.