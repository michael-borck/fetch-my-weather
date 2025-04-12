"""
Core functionality for simple-weather - A beginner-friendly Python package for weather data.

This module provides the main functions for fetching weather data and moon phases,
with built-in caching and error handling to make it suitable for educational use.
"""

import requests
import time
from urllib.parse import quote_plus

# --- Configuration ---
BASE_URL = "http://wttr.in/"
_CACHE_DURATION_SECONDS = 600  # Cache data for 10 minutes
_USER_AGENT = "simple-weather/0.1.0" # Be polite and identify our package

# --- In-memory Cache ---
# Simple dictionary to store cached responses
# Format: { "url": (timestamp, data) }
_cache = {}

# --- Configuration Functions ---

def set_cache_duration(seconds):
    """
    Set how long to cache weather data in seconds.
    
    Args:
        seconds (int): Duration in seconds. Set to 0 to disable caching.
        
    Returns:
        int: The new cache duration in seconds.
    """
    global _CACHE_DURATION_SECONDS
    _CACHE_DURATION_SECONDS = max(0, int(seconds))
    return _CACHE_DURATION_SECONDS

def set_user_agent(user_agent):
    """
    Set the User-Agent string sent with requests.
    
    Args:
        user_agent (str): The User-Agent string to use.
        
    Returns:
        str: The new User-Agent string.
    """
    global _USER_AGENT
    _USER_AGENT = str(user_agent)
    return _USER_AGENT

def clear_cache():
    """
    Clear all cached weather data.
    
    Returns:
        int: Number of entries cleared from cache.
    """
    global _cache
    count = len(_cache)
    _cache = {}
    return count

# --- Helper Functions ---

def _build_url(location="", units="", view_options="", lang=None,
               is_png=False, png_options="", is_moon=False,
               moon_date=None, moon_location_hint=None):
    """Constructs the full URL for the wttr.in request."""

    url = BASE_URL
    query_params = {}
    path_parts = []

    # --- Location Handling ---
    if is_moon:
        path = "/moon"
        if moon_date:
            path += f"@{moon_date}"
        if moon_location_hint:
             # Ensure hint starts correctly, remove leading '+' if present in input
            hint = moon_location_hint.lstrip(',')
            path += f",{quote_plus(hint)}"
        location_part = path
    elif location:
        # URL encode the location to handle spaces, special characters, unicode
        location_part = f"/{quote_plus(location)}"
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
        path_parts.append(location_part.lstrip('/')) # Remove leading slash for path joining
        if combined_options:
            path_parts.append(combined_options)
        if lang:
            path_parts.append(f"lang={lang}")
        
        # Join parts with '_' and add .png extension
        url += "_".join(path_parts) + ".png"

    else:
        # Text format uses query parameters
        url += location_part.lstrip('/') # Add location to path
        
        # Add options as query parameter string if any exist
        if combined_options:
           query_params['format_options'] = combined_options # Use a placeholder key first
        
        if lang:
            query_params['lang'] = lang

        # Build the query string
        if query_params:
             # Special handling for combined options which don't have a key in wttr.in
            query_string_parts = []
            if 'format_options' in query_params:
                query_string_parts.append(query_params['format_options'])
                del query_params['format_options'] # Remove placeholder
            
            # Add remaining key=value pairs
            query_string_parts.extend([f"{k}={v}" for k, v in query_params.items()])

            url += "?" + "&".join(query_string_parts)

    return url

def _get_from_cache(url):
    """Checks cache for non-expired data."""
    if _CACHE_DURATION_SECONDS <= 0:
        return None  # Caching disabled
        
    if url in _cache:
        timestamp, data = _cache[url]
        if time.time() - timestamp < _CACHE_DURATION_SECONDS:
            # Cache hit
            return data
        else:
            # Cache expired
            del _cache[url] # Remove expired entry
    return None

def _add_to_cache(url, data):
    """Adds data to the cache with current timestamp."""
    if _CACHE_DURATION_SECONDS > 0:  # Only cache if enabled
        _cache[url] = (time.time(), data)

# --- Public API Function ---

def get_weather(location: str = "",
                units: str = "",
                view_options: str = "",
                lang: str = None,
                is_png: bool = False,
                png_options: str = "",
                is_moon: bool = False,
                moon_date: str = None,
                moon_location_hint: str = None):
    """
    Fetches weather or moon phase information from wttr.in.

    Args:
        location (str): The location identifier (city, airport code, coordinates,
                        domain, area code, ~special name, or empty for current).
                        Ignored if is_moon is True.
        units (str): Units for output ('m' for metric, 'u' for USCS, 'M' for wind m/s).
        view_options (str): Combined view options (e.g., '0', '1', 'n', 'q', 'F', '0q').
        lang (str): Language code (e.g., 'fr', 'de', 'zh-cn').
        is_png (bool): If True, request a PNG image instead of text.
        png_options (str): PNG specific options (e.g., 'p', 't', 'transparency=100').
                           Only used if is_png is True.
        is_moon (bool): If True, fetch moon phase instead of weather.
        moon_date (str): Specific date for moon phase in 'YYYY-MM-DD' format.
                         Only used if is_moon is True.
        moon_location_hint (str): Location hint for moon phase (e.g., ',+US', ',+Paris').
                                  Only used if is_moon is True.

    Returns:
        str or bytes or None:
            - If successful and not PNG: Returns the weather report as a string.
            - If successful and PNG: Returns the PNG image data as bytes.
            - If an error occurs (network, bad response): Returns an error message string.
              No exceptions are raised.
    """
    # Input validation (optional but good practice)
    if units not in ["", "m", "u", "M"]:
         return "Error: Invalid 'units' parameter. Use 'm', 'u', or 'M'."
    # Add more validation as needed...

    # Build the request URL
    url = _build_url(location=location, units=units, view_options=view_options,
                     lang=lang, is_png=is_png, png_options=png_options,
                     is_moon=is_moon, moon_date=moon_date,
                     moon_location_hint=moon_location_hint)

    # Check cache first
    cached_data = _get_from_cache(url)
    if cached_data is not None:
        return cached_data

    # --- Perform the actual request ---
    headers = {
        'User-Agent': _USER_AGENT
    }
    # Add Accept-Language header if language is specified (alternative to ?lang=)
    # Note: ?lang= or subdomain is generally preferred by wttr.in documentation
    # if lang:
    #     headers['Accept-Language'] = lang

    try:
        response = requests.get(url, headers=headers, timeout=15) # 15 second timeout

        # Check if the request was successful (status code 2xx)
        if response.status_code >= 200 and response.status_code < 300:
            # Determine return type based on request
            if is_png:
                data = response.content # Return raw bytes for images
            else:
                data = response.text     # Return decoded text

            # Add successful response to cache
            _add_to_cache(url, data)
            return data
        else:
            # Handle non-successful status codes gracefully
            error_message = (f"Error fetching data from wttr.in: "
                             f"Status code {response.status_code} for URL {url}")
            # Maybe include response text if available and not too long?
            try:
                error_details = response.text[:200] # Limit details length
                if error_details:
                   error_message += f"\nResponse body (start): {error_details}"
            except Exception:
                pass # Ignore errors trying to get error details
            return error_message

    except requests.exceptions.Timeout:
        return f"Error: Request timed out while connecting to {url}"
    except requests.exceptions.ConnectionError:
        return f"Error: Could not connect to {url}. Check network connection."
    except requests.exceptions.RequestException as e:
        # Catch any other requests-related error
        return f"Error: An unexpected network error occurred: {e}"
    except Exception as e:
        # Catch any other unexpected error during processing
        # This shouldn't normally happen with the above catches, but belt-and-suspenders
        return f"Error: An unexpected error occurred: {e}"
