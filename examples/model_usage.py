#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Examples for using fetch-my-weather with Pydantic models.

This script demonstrates how to use the Pydantic models for accessing weather data
in a type-safe, structured way.
"""

import fetch_my_weather
from fetch_my_weather import (
    Astronomy,
    CurrentCondition,
    DailyForecast,
    HourlyForecast,
    NearestArea,
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

    # Disable mock mode
    fetch_my_weather.set_mock_mode(False)
    print("\nAll examples completed!")


if __name__ == "__main__":
    main()