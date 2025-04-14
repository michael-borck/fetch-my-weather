#!/usr/bin/env python
"""
Examples for using fetch-my-weather with Pydantic models.

This script demonstrates how to use the Pydantic models for accessing weather data
in a type-safe, structured way.
"""

import fetch_my_weather
from fetch_my_weather import (
    WeatherResponse,
)


def main() -> None:
    """Run the Pydantic model examples."""
    print("=== fetch-my-weather Pydantic Model Examples ===\n")

    # Enable mock mode to avoid hitting the API during testing
    fetch_my_weather.set_mock_mode(True)

    # Example 1: Get weather data as a Pydantic model
    print("Example 1: Get weather data as a Pydantic model")
    weather = fetch_my_weather.get_weather(location="London")

    # Verify we got a WeatherResponse object
    print(f"Response type: {type(weather)}")

    # We can use type hints to help our IDE and type checkers
    weather_response: WeatherResponse = weather

    # Example 1b: Get raw JSON weather data
    print("\nExample 1b: Get raw JSON weather data")
    # For the example, we'll create a sample JSON dictionary instead
    # of relying on the API call that returns differently in mock mode
    raw_weather = {
        "current_condition": [
            {
                "temp_C": "17",
                "temp_F": "63",
                "weatherDesc": [{"value": "Partly cloudy"}],
                "humidity": "71",
                "windspeedKmph": "11",
                "winddir16Point": "NE",
            }
        ]
    }

    # Verify we got a dictionary
    print(f"Response type: {type(raw_weather)}")
    if isinstance(raw_weather, dict):
        # Access and print some data using dictionary syntax
        print("Accessing data using dictionary syntax:")
        if "current_condition" in raw_weather and raw_weather["current_condition"]:
            condition = raw_weather["current_condition"][0]
            print(f"Temperature: {condition.get('temp_C')}°C")
            if "weatherDesc" in condition and condition["weatherDesc"]:
                print(f"Condition: {condition['weatherDesc'][0]['value']}")

    # Demonstrate accessing raw dictionary values vs. model attributes
    print("\nComparing access patterns:")
    print("Pydantic model: weather.current_condition[0].temp_C")
    print("Raw JSON dict: raw_weather['current_condition'][0]['temp_C']")

    # Example 2: Access current weather data
    print("\nExample 2: Access current weather data")
    if weather_response.current_condition:
        current = weather_response.current_condition[0]
        print(f"Temperature: {current.temp_C}C / {current.temp_F}F")

        if current.weatherDesc:
            print(f"Condition: {current.weatherDesc[0].value}")

        print(f"Humidity: {current.humidity}%")
        print(f"Wind: {current.windspeedKmph} km/h, {current.winddir16Point}")
    else:
        print("No current condition data available")

    # Example 3: Access location information
    print("\nExample 3: Access location information")
    if weather_response.nearest_area:
        location = weather_response.nearest_area[0]

        area_name = location.areaName[0].value if location.areaName else "Unknown"
        country = location.country[0].value if location.country else "Unknown"

        print(f"Location: {area_name}, {country}")
        print(f"Coordinates: {location.latitude}, {location.longitude}")
        print(f"Population: {location.population}")
    else:
        print("No location data available")

    # Example 4: Access forecast data
    print("\nExample 4: Access forecast data")
    if weather_response.weather:
        for i, day in enumerate(weather_response.weather):
            if i >= 3:  # Limit to 3 days
                break

            print(f"Date: {day.date}")
            print(f"  Temperature Range: {day.mintempC}C to {day.maxtempC}C")

            # Access astronomy data
            if day.astronomy:
                astronomy = day.astronomy[0]
                print(f"  Sunrise: {astronomy.sunrise}, Sunset: {astronomy.sunset}")
                print(f"  Moon phase: {astronomy.moon_phase}")

            # Access hourly forecast (just first entry)
            if day.hourly:
                hour = day.hourly[0]
                desc = hour.weatherDesc[0].value if hour.weatherDesc else "Unknown"
                print(f"  Hourly Example - Time: {hour.time}, Condition: {desc}")

            print()  # Add blank line between days
    else:
        print("No forecast data available")

    # Example 5: Access request information
    print("\nExample 5: Access request information")
    if weather_response.request:
        request_info = weather_response.request[0]
        print(f"Query: {request_info.query}")
        print(f"Query type: {request_info.type}")
    else:
        print("No request information available")

    # Disable mock mode
    fetch_my_weather.set_mock_mode(False)
    print("\nAll examples completed!")


if __name__ == "__main__":
    main()
