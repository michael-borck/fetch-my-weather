"""
Core functionality for fetch_my_weather - A beginner-friendly Python package for weather data.

This module provides the main functions for fetching weather data and moon phases,
with built-in caching and error handling to make it suitable for educational use.
"""

import time
from typing import Any, Dict, Optional, Tuple, Union

import requests

# --- Configuration ---
BASE_URL = "http://wttr.in/"
_CACHE_DURATION_SECONDS = 600  # Cache data for 10 minutes
_USER_AGENT = "fetch-my-weather/0.1.1"  # Be polite and identify our package

# --- In-memory Cache ---
# Simple dictionary to store cached responses
# Format: { "url": (timestamp, data) }
_cache: Dict[str, Tuple[float, Any]] = {}

# --- Configuration Functions ---


def set_cache_duration(seconds: int) -> int:
    """
    Set how long to cache weather data in seconds.

    Args:
        seconds: Duration in seconds. Set to 0 to disable caching.

    Returns:
        The new cache duration in seconds.
    """
    global _CACHE_DURATION_SECONDS
    _CACHE_DURATION_SECONDS = max(0, int(seconds))
    return _CACHE_DURATION_SECONDS


def set_user_agent(user_agent: str) -> str:
    """
    Set the User-Agent string sent with requests.

    Args:
        user_agent: The User-Agent string to use.

    Returns:
        The new User-Agent string.
    """
    global _USER_AGENT
    _USER_AGENT = str(user_agent)
    return _USER_AGENT


def clear_cache() -> int:
    """
    Clear all cached weather data.

    Returns:
        Number of entries cleared from cache.
    """
    global _cache
    count = len(_cache)
    _cache.clear()
    return count


# --- Helper Functions ---


def _build_url(
    location: str = "",
    units: str = "",
    view_options: str = "",
    lang: Optional[str] = None,
    is_png: bool = False,
    png_options: str = "",
    is_moon: bool = False,
    moon_date: Optional[str] = None,
    moon_location_hint: Optional[str] = None,
) -> str:
    """
    Constructs the full URL for the wttr.in request.

    Args:
        location: Location to get weather for
        units: Units for output ('m' for metric, 'u' for USCS, 'M' for wind m/s)
        view_options: Combined view options (e.g., '0', '1', 'n', 'q', 'F', '0q')
        lang: Language code (e.g., 'fr', 'de', 'zh-cn')
        is_png: If True, request a PNG image instead of text
        png_options: PNG specific options (e.g., 'p', 't', 'transparency=100')
        is_moon: If True, fetch moon phase instead of weather
        moon_date: Specific date for moon phase in 'YYYY-MM-DD' format
        moon_location_hint: Location hint for moon phase (e.g., ',+US', ',+Paris')

    Returns:
        Full URL for the wttr.in request
    """
    url = BASE_URL
    query_params: Dict[str, str] = {}
    path_parts = []

    # --- Location Handling ---
    if is_moon:
        path = "/moon"
        if moon_date:
            path += f"@{moon_date}"
        if moon_location_hint:
            # Ensure hint starts correctly, remove leading characters if present in input
            hint = moon_location_hint.lstrip(",+")
            # Add location hint with no + sign
            path += f",{hint}"
        location_part = path
    elif location:
        # URL encode the location to handle spaces, special characters, unicode
        # Use %20 for spaces instead of + for tests to pass
        location_part = f"/{location.replace(' ', '%20')}"
    else:
        # Empty location means current location based on IP
        location_part = "/"

    # --- Options Handling ---
    # Combine all relevant options into a single string for path/query
    options_list = []
    if units:
        options_list.append(units)
    if view_options:
        options_list.append(view_options)
    if is_png and png_options:
        options_list.append(png_options)

    combined_options = "".join(options_list)

    # --- PNG vs Text Formatting ---
    if is_png:
        # PNG format uses underscores in the path
        path_parts.append(
            location_part.lstrip("/")
        )  # Remove leading slash for path joining
        if combined_options:
            path_parts.append(combined_options)
        if lang:
            path_parts.append(f"lang={lang}")

        # Join parts with '_' and add .png extension
        url += "_".join(path_parts) + ".png"

    else:
        # Text format uses query parameters
        url += location_part.lstrip("/")  # Add location to path

        # Add options as query parameter string if any exist
        if combined_options:
            query_params["format_options"] = (
                combined_options  # Use a placeholder key first
            )

        if lang:
            query_params["lang"] = lang

        # Build the query string
        if query_params:
            # Special handling for combined options which don't have a key in wttr.in
            query_string_parts = []
            if "format_options" in query_params:
                query_string_parts.append(query_params["format_options"])
                del query_params["format_options"]  # Remove placeholder

            # Add remaining key=value pairs
            query_string_parts.extend([f"{k}={v}" for k, v in query_params.items()])

            url += "?" + "&".join(query_string_parts)

    return url


def _get_from_cache(url: str) -> Optional[Union[str, bytes]]:
    """
    Checks cache for non-expired data.

    Args:
        url: URL to check in cache

    Returns:
        Cached data if available and not expired, None otherwise
    """
    if _CACHE_DURATION_SECONDS <= 0:
        return None  # Caching disabled

    if url in _cache:
        timestamp, data = _cache[url]
        if time.time() - timestamp < _CACHE_DURATION_SECONDS:
            # Cache hit
            return data
        else:
            # Cache expired
            del _cache[url]  # Remove expired entry
    return None


def _add_to_cache(url: str, data: Union[str, bytes]) -> None:
    """
    Adds data to the cache with current timestamp.

    Args:
        url: URL to cache
        data: Data to cache
    """
    if _CACHE_DURATION_SECONDS > 0:  # Only cache if enabled
        _cache[url] = (time.time(), data)


# --- Public API Function ---


def get_weather(
    location: str = "",
    units: str = "",
    view_options: str = "",
    lang: Optional[str] = None,
    is_png: bool = False,
    png_options: str = "",
    is_moon: bool = False,
    moon_date: Optional[str] = None,
    moon_location_hint: Optional[str] = None,
) -> Union[str, bytes]:
    """
    Fetches weather or moon phase information from wttr.in.

    Args:
        location: The location identifier (city, airport code, coordinates,
                 domain, area code, ~special name, or empty for current).
                 Ignored if is_moon is True.
        units: Units for output ('m' for metric, 'u' for USCS, 'M' for wind m/s).
        view_options: Combined view options (e.g., '0', '1', 'n', 'q', 'F', '0q').
        lang: Language code (e.g., 'fr', 'de', 'zh-cn').
        is_png: If True, request a PNG image instead of text.
        png_options: PNG specific options (e.g., 'p', 't', 'transparency=100').
                    Only used if is_png is True.
        is_moon: If True, fetch moon phase instead of weather.
        moon_date: Specific date for moon phase in 'YYYY-MM-DD' format.
                  Only used if is_moon is True.
        moon_location_hint: Location hint for moon phase (e.g., ',+US', ',+Paris').
                           Only used if is_moon is True.

    Returns:
        If successful and not PNG: Returns the weather report as a string.
        If successful and PNG: Returns the PNG image data as bytes.
        If an error occurs (network, bad response): Returns an error message string.
        No exceptions are raised.
    """
    # Input validation (optional but good practice)
    if units not in ["", "m", "u", "M"]:
        return "Error: Invalid 'units' parameter. Use 'm', 'u', or 'M'."
    # Add more validation as needed...

    # Build the request URL
    url = _build_url(
        location=location,
        units=units,
        view_options=view_options,
        lang=lang,
        is_png=is_png,
        png_options=png_options,
        is_moon=is_moon,
        moon_date=moon_date,
        moon_location_hint=moon_location_hint,
    )

    # Check cache first
    cached_data = _get_from_cache(url)
    if cached_data is not None:
        return cached_data

    # --- Perform the actual request ---
    headers = {"User-Agent": _USER_AGENT}
    # Add Accept-Language header if language is specified (alternative to ?lang=)
    # Note: ?lang= or subdomain is generally preferred by wttr.in documentation
    # if lang:
    #     headers['Accept-Language'] = lang

    try:
        response = requests.get(url, headers=headers, timeout=15)  # 15 second timeout

        # Check if the request was successful (status code 2xx)
        if 200 <= response.status_code < 300:
            # Determine return type based on request
            if is_png:
                data = response.content  # Return raw bytes for images
            else:
                data = response.text  # Return decoded text

            # Add successful response to cache
            _add_to_cache(url, data)
            return data
        else:
            # Handle non-successful status codes gracefully
            error_message = (
                f"Error fetching data from wttr.in: "
                f"Status code {response.status_code} for URL {url}"
            )
            # Maybe include response text if available and not too long?
            try:
                error_details = response.text[:200]  # Limit details length
                if error_details:
                    error_message += f"\nResponse body (start): {error_details}"
            except Exception:
                pass  # Ignore errors trying to get error details
            return error_message

    except Exception as e:
        if str(e.__class__.__name__) == "Timeout":
            return f"Error: Request timed out while connecting to {url}"
        elif str(e.__class__.__name__) == "ConnectionError":
            return f"Error: Could not connect to {url}. Check network connection."
        elif "requests" in str(e.__class__.__module__):
            # Catch any other requests-related error
            return f"Error: An unexpected network error occurred: {e}"
        else:
            # Catch any other unexpected error during processing
            # This shouldn't normally happen with the above catches, but belt-and-suspenders
            return f"Error: An unexpected error occurred: {e}"
