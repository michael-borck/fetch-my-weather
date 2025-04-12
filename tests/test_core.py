"""
Tests for the core functionality of the fetch-my-weather package.
"""

import time

from pytest_mock import MockerFixture

# Import the package
from fetch_my_weather.core import (
    _build_url,
    _cache,
    clear_cache,
    get_weather,
    set_cache_duration,
    set_user_agent,
)


class TestCoreConfiguration:
    """Tests for the configuration functions."""

    def test_set_cache_duration(self) -> None:
        """Test setting cache duration."""
        # Save original value to restore later
        original_duration = set_cache_duration(0)

        # Test setting to 0 (disabled)
        assert set_cache_duration(0) == 0

        # Test setting to a positive value
        assert set_cache_duration(300) == 300

        # Test setting to a negative value (should be converted to 0)
        assert set_cache_duration(-10) == 0

        # Restore original value
        set_cache_duration(original_duration)

    def test_set_user_agent(self) -> None:
        """Test setting the user agent."""
        # Save original value to restore later
        original_agent = set_user_agent("test-agent")

        # Test setting to a string
        assert set_user_agent("my-app") == "my-app"

        # Test setting to a non-string (should be converted to string)
        assert set_user_agent(123) == "123"

        # Restore original value
        set_user_agent(original_agent)

    def test_clear_cache(self) -> None:
        """Test clearing the cache."""
        # Ensure cache is empty
        clear_cache()
        assert len(_cache) == 0

        # Add some items to cache
        _cache["test_url1"] = (time.time(), "data1")
        _cache["test_url2"] = (time.time(), "data2")

        # Clear cache and verify
        assert clear_cache() == 2
        assert len(_cache) == 0


class TestUrlBuilder:
    """Tests for the URL building functionality."""

    def test_basic_url(self) -> None:
        """Test building a basic URL for weather."""
        url = _build_url()
        assert url == "http://wttr.in/"

    def test_location_url(self) -> None:
        """Test building a URL with a location."""
        url = _build_url(location="London")
        assert url == "http://wttr.in/London"

    def test_location_with_spaces(self) -> None:
        """Test building a URL with a location that contains spaces."""
        url = _build_url(location="New York")
        assert "New%20York" in url

    def test_units_option(self) -> None:
        """Test building a URL with units option."""
        url = _build_url(location="Berlin", units="m")
        assert url == "http://wttr.in/Berlin?m"

    def test_view_options(self) -> None:
        """Test building a URL with view options."""
        url = _build_url(location="Paris", view_options="0")
        assert url == "http://wttr.in/Paris?0"

    def test_combined_options(self) -> None:
        """Test building a URL with combined options."""
        url = _build_url(location="Rome", units="m", view_options="0")
        assert url == "http://wttr.in/Rome?m0"

    def test_lang_option(self) -> None:
        """Test building a URL with language option."""
        url = _build_url(location="Tokyo", lang="ja")
        assert url == "http://wttr.in/Tokyo?lang=ja"

    def test_combined_with_lang(self) -> None:
        """Test building a URL with combined options and language."""
        url = _build_url(location="Madrid", units="m", view_options="0", lang="es")
        assert "Madrid" in url
        assert "m0" in url
        assert "lang=es" in url

    def test_png_url(self) -> None:
        """Test building a URL for PNG format."""
        url = _build_url(location="Sydney", is_png=True)
        assert url == "http://wttr.in/Sydney.png"

    def test_png_with_options(self) -> None:
        """Test building a URL for PNG format with options."""
        url = _build_url(location="Cairo", is_png=True, png_options="t")
        assert url == "http://wttr.in/Cairo_t.png"

    def test_moon_url(self) -> None:
        """Test building a URL for moon phase."""
        url = _build_url(is_moon=True)
        assert url == "http://wttr.in/moon"

    def test_moon_with_date(self) -> None:
        """Test building a URL for moon phase with a specific date."""
        url = _build_url(is_moon=True, moon_date="2025-12-25")
        assert url == "http://wttr.in/moon@2025-12-25"

    def test_moon_with_location_hint(self) -> None:
        """Test building a URL for moon phase with a location hint."""
        url = _build_url(is_moon=True, moon_location_hint=",+Paris")
        assert "moon,Paris" in url


class TestWeatherFetching:
    """Tests for the weather fetching functionality."""

    def test_get_weather_invalid_units(self) -> None:
        """Test get_weather with invalid units."""
        result = get_weather(units="invalid")
        assert isinstance(result, str)
        assert "Error: Invalid 'units' parameter" in result

    def test_get_weather_success(self, mocker: MockerFixture) -> None:
        """Test get_weather with a successful response."""
        # Mock requests.get
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = "Weather data for location"
        mocker.patch("requests.get", return_value=mock_response)

        # Get weather
        result = get_weather(location="TestCity")

        # Verify result
        assert result == "Weather data for location"

    def test_get_weather_png(self, mocker: MockerFixture) -> None:
        """Test get_weather with PNG format."""
        # Mock requests.get
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.content = b"PNG image data"
        mocker.patch("requests.get", return_value=mock_response)

        # Get weather as PNG
        result = get_weather(location="TestCity", is_png=True)

        # Verify result
        assert result == b"PNG image data"

    def test_get_weather_error_response(self, mocker: MockerFixture) -> None:
        """Test get_weather with an error response."""
        # Mock requests.get
        mock_response = mocker.Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mocker.patch("requests.get", return_value=mock_response)

        # Get weather
        result = get_weather(location="NonExistentCity")

        # Verify result
        assert isinstance(result, str)
        assert "Error fetching data" in result
        assert "404" in result

    def test_get_weather_network_timeout(self, mocker: MockerFixture) -> None:
        """Test get_weather with a network timeout."""
        # Create a mock exception that has a __class__.__name__ of "Timeout"
        class MockTimeoutError(Exception):
            pass

        # Rename the class to match what our code is looking for
        MockTimeoutError.__name__ = "Timeout"

        # Mock requests.get to raise our custom Timeout
        mocker.patch("requests.get", side_effect=MockTimeoutError())

        # Get weather
        result = get_weather()

        # Verify result
        assert isinstance(result, str)
        assert "Error: Request timed out" in result

    def test_get_weather_connection_error(self, mocker: MockerFixture) -> None:
        """Test get_weather with a connection error."""
        # Create a mock exception that has a __class__.__name__ of "ConnectionError"
        class MockNetworkError(Exception):
            pass

        # Rename the class to match what our code is looking for
        MockNetworkError.__name__ = "ConnectionError"

        # Mock requests.get to raise our custom ConnectionError
        mocker.patch("requests.get", side_effect=MockNetworkError())

        # Get weather
        result = get_weather()

        # Verify result
        assert isinstance(result, str)
        assert "Error: Could not connect" in result

    def test_get_weather_caching(self, mocker: MockerFixture) -> None:
        """Test that weather data is cached correctly."""
        # Set cache duration
        set_cache_duration(300)

        # Clear cache
        clear_cache()

        # Mock requests.get
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = "Cached weather data"
        mock_get = mocker.patch("requests.get", return_value=mock_response)

        # First call should make a request
        result1 = get_weather(location="CacheTest")
        assert result1 == "Cached weather data"
        assert mock_get.call_count == 1

        # Second call should use cache
        result2 = get_weather(location="CacheTest")
        assert result2 == "Cached weather data"
        assert mock_get.call_count == 1  # Still 1, no new request

        # Restore cache duration
        set_cache_duration(600)
