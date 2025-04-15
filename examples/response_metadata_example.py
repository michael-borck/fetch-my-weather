#!/usr/bin/env python
"""
Example demonstrating the response metadata feature.

This script shows how to use the metadata feature to check whether responses
are real API data, cached data, or mock/fallback data.
"""

import fetch_my_weather
from fetch_my_weather import ResponseWrapper


def main() -> None:
    """Run examples of using the response metadata feature."""
    print("=== fetch-my-weather Response Metadata Examples ===\n")

    # Example 1: Getting response with metadata
    print("Example 1: Getting response with metadata")
    response = fetch_my_weather.get_weather(
        location="Paris",
        with_metadata=True,  # This enables the metadata feature
    )

    # Response is now a ResponseWrapper object
    print(f"Response type: {type(response)}")
    if isinstance(response, ResponseWrapper):
        # Access the metadata
        metadata = response.metadata
        print(f"Real API data: {metadata.is_real_data}")
        print(f"Cached data: {metadata.is_cached}")
        print(f"Mock data: {metadata.is_mock}")
        if metadata.status_code:
            print(f"Status code: {metadata.status_code}")
        print(f"Requested URL: {metadata.url}")
        print(f"Timestamp: {metadata.timestamp}")

        # Access the actual data
        data = response.data
        if hasattr(data, "current_condition") and data.current_condition:
            current = data.current_condition[0]
            print(f"Temperature: {current.temp_C}°C")

    print()

    # Example 2: Handling errors gracefully
    print("Example 2: Handling errors gracefully with fallback data")
    # Intentionally use an invalid location but with metadata enabled
    invalid_response = fetch_my_weather.get_weather(
        location="NonExistentPlace123456789", with_metadata=True
    )

    if isinstance(invalid_response, ResponseWrapper):
        metadata = invalid_response.metadata
        if metadata.error_type:
            print(f"Error occurred: {metadata.error_type}")
            print(f"Error message: {metadata.error_message}")

        # Even though there was an error, we can still access weather data
        # because the system fallback to mock data
        print("Data is still available despite the error:")
        data = invalid_response.data
        if hasattr(data, "current_condition") and data.current_condition:
            current = data.current_condition[0]
            print(f"Temperature: {current.temp_C}°C (mock data)")

    print()

    # Example 3: Rate limiting handling
    print("Example 3: Simulating rate limiting (503 error)")
    # We'll use mock mode with a special flag to simulate rate limiting
    fetch_my_weather.set_mock_mode(False)  # Ensure mock mode is off

    # This is a hypothetical example - in a real situation, you'd hit the rate limit naturally
    # For this example, if the API returns an error, our code will handle it gracefully
    rate_limited_response = fetch_my_weather.get_weather(
        location="Sydney", with_metadata=True
    )

    if isinstance(rate_limited_response, ResponseWrapper):
        metadata = rate_limited_response.metadata
        print(f"Data source: {'Mock' if metadata.is_mock else 'Real API'}")
        print(f"Error type: {metadata.error_type or 'None'}")

        # Still able to use the data regardless of the source
        data = rate_limited_response.data
        if hasattr(data, "current_condition") and data.current_condition:
            current = data.current_condition[0]
            print(f"Temperature: {current.temp_C}°C")

    # Reset mock mode
    fetch_my_weather.set_mock_mode(False)
    print("\nAll examples completed!")


if __name__ == "__main__":
    main()
