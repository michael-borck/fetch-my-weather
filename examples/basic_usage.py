"""
Basic usage examples for the fetch-my-weather package.

This script demonstrates the most common ways to use the fetch-my-weather package
to fetch weather data.
"""

import json
import time

import fetch_my_weather


def main() -> None:
    """Run the basic usage examples."""
    print("=== fetch-my-weather Basic Usage Examples ===\n")

    # Example 1: Current location weather as Pydantic model (based on IP)
    print("Example 1: Current location weather as Pydantic model (based on IP)")
    weather = (
        fetch_my_weather.get_weather()
    )  # Default format is now 'json' which returns Pydantic model
    if hasattr(weather, "current_condition"):
        print("Weather data received as Pydantic model:")
        # Extract some key information using Pydantic model property access
        if weather.current_condition:
            current = weather.current_condition[0]
            print(f"Temperature: {current.temp_C}°C / {current.temp_F}°F")

            if current.weatherDesc:
                print(f"Condition: {current.weatherDesc[0].value}")

            print(f"Humidity: {current.humidity}%")
            print(f"Wind: {current.windspeedKmph} km/h, {current.winddir16Point}")

        # Print the model as JSON for reference
        print("\nModel as JSON:")
        try:
            # Pydantic v2 compatibility
            if hasattr(weather, "model_dump_json"):
                print(weather.model_dump_json(indent=2))
            # Pydantic v1 compatibility
            else:
                print(weather.json())
        except Exception as e:
            print(f"(Error converting model to JSON: {e})")
    else:
        print(f"Could not get current weather: {weather}")

    # Example 1b: Current location weather in raw JSON format (based on IP)
    print("\nExample 1b: Current location weather in raw JSON format (based on IP)")
    # For the example, we'll create a sample dictionary to illustrate the raw_json mode
    # In real usage, you would use: fetch_my_weather.get_weather(format="raw_json")
    # with real API calls, but for mock mode testing we'll use this sample:
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

    print("Weather data received as raw JSON (Python dictionary):")
    # Extract some key information from the JSON
    if "current_condition" in raw_weather and raw_weather["current_condition"]:
        current = raw_weather["current_condition"][0]
        print(
            f"Temperature: {current.get('temp_C', 'N/A')}°C / {current.get('temp_F', 'N/A')}°F"
        )
        print(f"Condition: {current.get('weatherDesc', [{}])[0].get('value', 'N/A')}")
        print(f"Humidity: {current.get('humidity', 'N/A')}%")
        print(
            f"Wind: {current.get('windspeedKmph', 'N/A')} km/h, {current.get('winddir16Point', 'N/A')}"
        )

    # Print the full JSON for reference (pretty-printed)
    print("\nFull raw JSON response:")
    print(json.dumps(raw_weather, indent=2))

    # Note: With a real API call outside of mock mode, you would use:
    # raw_weather = fetch_my_weather.get_weather(format="raw_json")
    # which returns a Python dictionary without Pydantic model conversion
    print("\n" + "-" * 50 + "\n")

    # Example 2: Weather for a specific city in text format
    print("Example 2: Weather for Paris in text format")
    paris_weather = fetch_my_weather.get_weather(location="Paris", format="text")
    if isinstance(paris_weather, str) and not paris_weather.startswith("Error:"):
        print(paris_weather)
    else:
        print(f"Could not get Paris weather: {paris_weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 3: Weather with options (compact view, metric units) in JSON
    print("Example 3: Compact weather for Berlin (metric units) in JSON")
    berlin_weather = fetch_my_weather.get_weather(
        location="Berlin", view_options="0", units="m", format="json"
    )
    if isinstance(berlin_weather, dict):
        # Extract forecast information
        if "weather" in berlin_weather:
            print("Weather forecast for Berlin:")
            for day in berlin_weather.get("weather", []):
                date = day.get("date", "N/A")
                max_temp = day.get("maxtempC", "N/A")
                min_temp = day.get("mintempC", "N/A")
                desc = (
                    day.get("hourly", [{}])[0]
                    .get("weatherDesc", [{}])[0]
                    .get("value", "N/A")
                )
                print(
                    f"Date: {date}, Min: {min_temp}°C, Max: {max_temp}°C, Condition: {desc}"
                )
    else:
        print(f"Could not get Berlin weather: {berlin_weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 4: Weather in a different language
    print("Example 4: Weather for Tokyo in Japanese")
    tokyo_weather = fetch_my_weather.get_weather(location="Tokyo", lang="ja")
    if isinstance(tokyo_weather, str) and not tokyo_weather.startswith("Error:"):
        print(tokyo_weather)
    else:
        print(f"Could not get Tokyo weather: {tokyo_weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 5: Moon phase
    print("Example 5: Current moon phase")
    moon = fetch_my_weather.get_weather(is_moon=True)
    if isinstance(moon, str) and not moon.startswith("Error:"):
        print(moon)
    else:
        print(f"Could not get moon phase: {moon}")
    print("\n" + "-" * 50 + "\n")

    # Example 6: Moon phase for a specific date
    print("Example 6: Moon phase for December 25, 2025")
    xmas_moon = fetch_my_weather.get_weather(is_moon=True, moon_date="2025-12-25")
    if isinstance(xmas_moon, str) and not xmas_moon.startswith("Error:"):
        print(xmas_moon)
    else:
        print(f"Could not get Christmas moon phase: {xmas_moon}")
    print("\n" + "-" * 50 + "\n")

    # Example 7: PNG weather image (save to file) using format parameter
    print("Example 7: Weather as PNG image using format parameter")
    city_png = fetch_my_weather.get_weather(location="Paris", format="png")
    if isinstance(city_png, bytes):
        file_size = len(city_png)
        print(f"Successfully fetched Paris weather as PNG ({file_size} bytes)")
        try:
            with open("paris_weather.png", "wb") as f:
                f.write(city_png)
            print("Saved paris_weather.png")
        except OSError as e:
            print(f"Error saving PNG: {e}")
    else:
        print(f"Could not get Paris PNG: {city_png}")
    print("\n" + "-" * 50 + "\n")

    # Example 8: Caching demonstration
    print("Example 8: Caching demonstration")
    print("Setting cache duration to 5 seconds for demonstration...")
    fetch_my_weather.set_cache_duration(5)

    print("First request for New York weather:")
    start_time = time.time()
    fetch_my_weather.get_weather(location="New York")
    request1_time = time.time() - start_time
    print(f"Request completed in {request1_time:.2f} seconds")

    print("\nSecond request (should use cache):")
    start_time = time.time()
    fetch_my_weather.get_weather(location="New York")
    request2_time = time.time() - start_time
    print(f"Request completed in {request2_time:.2f} seconds")

    print("\nWaiting 6 seconds for cache to expire...")
    time.sleep(6)

    print("\nThird request (cache should have expired):")
    start_time = time.time()
    fetch_my_weather.get_weather(location="New York")
    request3_time = time.time() - start_time
    print(f"Request completed in {request3_time:.2f} seconds")

    # Reset cache duration to default
    fetch_my_weather.set_cache_duration(600)

    print("\n" + "-" * 50 + "\n")

    # Example 9: Mock data functionality
    print("Example 9: Mock data functionality")
    print("Enabling mock data mode...")
    fetch_my_weather.set_mock_mode(True)

    print("\nMock JSON data:")
    mock_json = fetch_my_weather.get_weather(location="AnyCity")
    if isinstance(mock_json, dict):
        # Extract and print some key information
        current = mock_json["current_condition"][0]
        print(f"Temperature: {current['temp_C']}°C")
        print(f"Condition: {current['weatherDesc'][0]['value']}")
        print(
            f"Location: {mock_json['nearest_area'][0]['areaName'][0]['value']}, "
            + f"{mock_json['nearest_area'][0]['country'][0]['value']}"
        )
        if "mock_data_notice" in mock_json:
            print(f"Notice: {mock_json['mock_data_notice']}")

    print("\nMock text data:")
    mock_text = fetch_my_weather.get_weather(location="AnyCity", format="text")
    print(mock_text)

    print("\nMock PNG data (sample):")
    mock_png = fetch_my_weather.get_weather(location="AnyCity", format="png")
    print(f"Received {len(mock_png)} bytes of mock PNG data")

    # Disable mock mode
    print("\nDisabling mock data mode...")
    fetch_my_weather.set_mock_mode(False)
    print("\n" + "-" * 50 + "\n")

    # Example 10: Error handling (intentional error)
    print("Example 10: Error handling demonstration")
    bad_result = fetch_my_weather.get_weather(
        location="ThisPlaceDefinitelyDoesNotExist12345"
    )
    print("Result from invalid location request:")
    print(bad_result)
    print("\n" + "-" * 50 + "\n")

    print("All examples completed!")


if __name__ == "__main__":
    main()
