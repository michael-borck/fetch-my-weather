"""
Pytest configuration file for fetch-my-weather tests.
"""

from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True)
def reset_cache() -> Iterator[None]:
    """
    Reset the cache before and after each test.

    This is an autouse fixture that will run for every test.
    It ensures that tests don't affect each other through cached data.
    """
    # Import here to avoid circular imports
    from fetch_my_weather.core import clear_cache, set_cache_duration

    # Store original cache duration
    original_duration = set_cache_duration(600)

    # Clear cache before test
    clear_cache()

    # Run the test
    yield

    # Clear cache after test and restore original duration
    clear_cache()
    set_cache_duration(original_duration)
