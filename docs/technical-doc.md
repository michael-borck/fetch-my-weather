# Technical Documentation for fetch-my-weather

This document provides technical details about the implementation of the `fetch-my-weather` package. It's intended for developers who want to understand the internal workings of the package or who might want to contribute to its development.

## Architecture Overview

`fetch-my-weather` is intentionally designed with a simple, flat architecture consisting of a small number of public functions and a few private helper functions.

### File Structure

```
src/fetch_my_weather/
├── __init__.py      # Exports public API
└── core.py          # Core implementation
```

### Module Layout

- **__init__.py**: Exports the public API functions and package metadata
- **core.py**: Contains all implementation code, including public API functions and private helper functions

## Data Flow

The basic flow of data through the package is:

1. User calls `get_weather()` with parameters
2. Parameters are validated
3. URL is constructed using `_build_url()`
4. Cache is checked using `_get_from_cache()`
5. If data is not in cache, HTTP request is made
6. Response is processed
7. Response is stored in cache using `_add_to_cache()`
8. Data is returned to the user

```
┌─────────────┐    ┌───────────────┐    ┌─────────────┐
│ get_weather ├───►│   _build_url  ├───►│ Cache Check │
└─────────────┘    └───────────────┘    └──────┬──────┘
                                                │
                                                ▼
┌─────────────┐    ┌───────────────┐    ┌─────────────┐
│ Return Data │◄───┤ _add_to_cache │◄───┤ HTTP Request│
└─────────────┘    └───────────────┘    └─────────────┘
```

## Key Components

### 1. URL Construction

The `_build_url()` function handles the complex logic of constructing proper URLs for the weather service. It takes into account:

- Location specification
- Option formatting
- PNG vs text mode differences
- Moon phase requests
- Language settings

This function is critical because the weather service has different URL formats depending on the type of request.

### 2. Caching System

The caching system consists of:

- A module-level dictionary `_cache` that stores responses
- `_get_from_cache()` function to retrieve cached data
- `_add_to_cache()` function to store new data
- Cache duration setting that controls expiration
- Public `clear_cache()` function to manually clear the cache

The cache uses URLs as keys and stores tuples of `(timestamp, data)` as values. This allows for time-based expiration of cache entries.

### 3. HTTP Request Handling

HTTP requests are made using the `requests` library. This section of the code:

- Sets appropriate headers (User-Agent)
- Makes the GET request with timeout
- Processes the response based on content type (text vs binary)
- Handles various error conditions

### 4. Error Handling

The package uses a consistent approach to error handling:

- No exceptions are raised to the user
- All errors are caught and converted to descriptive error messages
- Error messages are returned as strings that start with "Error:"
- HTTP errors include status codes
- Network errors include details about the failure

## Implementation Details

### In-memory Cache

The cache is implemented as a simple in-memory dictionary. This approach was chosen for simplicity and educational value. It means:

- Cache is not persistent across program restarts
- Cache is not shared between different processes
- Cache size is not explicitly limited (could grow large with many requests)

```python
# Format: { "url": (timestamp, data) }
_cache = {}
```

### Error Return Pattern

Instead of using exceptions, the package returns error information using a pattern recognition approach:

```python
# To return an error
return f"Error: {error_message}"

# To check for errors
if isinstance(result, str) and result.startswith("Error:"):
    # Handle error
else:
    # Process valid result
```

This pattern was chosen to make error handling more accessible to beginners.

### Content Type Detection

The package uses the request parameter `is_png` to determine how to process the response:

```python
if is_png:
    data = response.content  # Return raw bytes for images
else:
    data = response.text     # Return decoded text
```

## Performance Considerations

### Network Efficiency

The built-in caching mechanism is designed to reduce network requests for identical queries, which:
- Improves response times for repeated requests
- Reduces load on the weather service
- Helps avoid rate limiting

### Memory Usage

The in-memory cache can potentially consume significant memory if many different locations are queried and cached. Consider:

- Cache sizes are proportional to the response size (which can vary)
- No automatic pruning of old entries (only expiration-based removal)
- No size-based eviction policy

## Testing

The package includes unit tests that focus on:

1. URL construction
2. Cache functionality
3. Response handling
4. Error handling

Tests use mocking to avoid making actual network requests, ensuring tests are fast and reliable.

## Extensibility

The package was designed with teaching in mind rather than extensibility, but it could be extended in several ways:

1. Adding support for additional weather services
2. Implementing more sophisticated caching (e.g., persistent cache)
3. Adding structured data parsing for weather information
4. Supporting more output formats

## Dependencies

The only external dependency is the `requests` library, which was chosen for its simplicity and widespread use. This minimizes installation issues and keeps the package lightweight.
