"""
Basic usage examples for the simple-weather package.

This script demonstrates the most common ways to use the simple-weather package
to fetch weather data.
"""

import time

import simple_weather


def main() -> None:
    """Run the basic usage examples."""
    print("=== simple-weather Basic Usage Examples ===\n")

    # Example 1: Current location weather (based on IP)
    print("Example 1: Current location weather (based on IP)")
    weather = simple_weather.get_weather()
    if isinstance(weather, str) and not weather.startswith("Error:"):
        print(weather)
    else:
        print(f"Could not get current weather: {weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 2: Weather for a specific city
    print("Example 2: Weather for Paris")
    paris_weather = simple_weather.get_weather(location="Paris")
    if isinstance(paris_weather, str) and not paris_weather.startswith("Error:"):
        print(paris_weather)
    else:
        print(f"Could not get Paris weather: {paris_weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 3: Weather with options (compact view, metric units)
    print("Example 3: Compact weather for Berlin (metric units)")
    berlin_weather = simple_weather.get_weather(
        location="Berlin", view_options="0", units="m"
    )
    if isinstance(berlin_weather, str) and not berlin_weather.startswith("Error:"):
        print(berlin_weather)
    else:
        print(f"Could not get Berlin weather: {berlin_weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 4: Weather in a different language
    print("Example 4: Weather for Tokyo in Japanese")
    tokyo_weather = simple_weather.get_weather(location="Tokyo", lang="ja")
    if isinstance(tokyo_weather, str) and not tokyo_weather.startswith("Error:"):
        print(tokyo_weather)
    else:
        print(f"Could not get Tokyo weather: {tokyo_weather}")
    print("\n" + "-" * 50 + "\n")

    # Example 5: Moon phase
    print("Example 5: Current moon phase")
    moon = simple_weather.get_weather(is_moon=True)
    if isinstance(moon, str) and not moon.startswith("Error:"):
        print(moon)
    else:
        print(f"Could not get moon phase: {moon}")
    print("\n" + "-" * 50 + "\n")

    # Example 6: Moon phase for a specific date
    print("Example 6: Moon phase for December 25, 2025")
    xmas_moon = simple_weather.get_weather(is_moon=True, moon_date="2025-12-25")
    if isinstance(xmas_moon, str) and not xmas_moon.startswith("Error:"):
        print(xmas_moon)
    else:
        print(f"Could not get Christmas moon phase: {xmas_moon}")
    print("\n" + "-" * 50 + "\n")

    # Example 7: PNG weather image (save to file)
    print("Example 7: Weather as PNG image")
    london_png = simple_weather.get_weather(location="London", is_png=True)
    if isinstance(london_png, bytes):
        file_size = len(london_png)
        print(f"Successfully fetched London weather as PNG ({file_size} bytes)")
        try:
            with open("london_weather.png", "wb") as f:
                f.write(london_png)
            print("Saved london_weather.png")
        except OSError as e:
            print(f"Error saving PNG: {e}")
    else:
        print(f"Could not get London PNG: {london_png}")
    print("\n" + "-" * 50 + "\n")

    # Example 8: Caching demonstration
    print("Example 8: Caching demonstration")
    print("Setting cache duration to 5 seconds for demonstration...")
    simple_weather.set_cache_duration(5)

    print("First request for New York weather:")
    start_time = time.time()
    simple_weather.get_weather(location="New York")
    request1_time = time.time() - start_time
    print(f"Request completed in {request1_time:.2f} seconds")

    print("\nSecond request (should use cache):")
    start_time = time.time()
    simple_weather.get_weather(location="New York")
    request2_time = time.time() - start_time
    print(f"Request completed in {request2_time:.2f} seconds")

    print("\nWaiting 6 seconds for cache to expire...")
    time.sleep(6)

    print("\nThird request (cache should have expired):")
    start_time = time.time()
    simple_weather.get_weather(location="New York")
    request3_time = time.time() - start_time
    print(f"Request completed in {request3_time:.2f} seconds")

    # Reset cache duration to default
    simple_weather.set_cache_duration(600)

    print("\n" + "-" * 50 + "\n")

    # Example 9: Error handling (intentional error)
    print("Example 9: Error handling demonstration")
    bad_result = simple_weather.get_weather(
        location="ThisPlaceDefinitelyDoesNotExist12345"
    )
    print("Result from invalid location request:")
    print(bad_result)
    print("\n" + "-" * 50 + "\n")

    print("All examples completed!")


if __name__ == "__main__":
    main()
