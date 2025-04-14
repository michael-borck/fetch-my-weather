# Technical Documentation for fetch-my-weather

This document provides technical details about the implementation of the `fetch-my-weather` package. It's intended for developers who want to understand the internal workings of the package or who might want to contribute to its development.

## Architecture Overview

`fetch-my-weather` is intentionally designed with a simple, structured architecture consisting of public functions, Pydantic models, and a few private helper functions.

### File Structure

```
src/fetch_my_weather/
├── __init__.py      # Exports public API and models
├── core.py          # Core implementation
└── models.py        # Pydantic data models
```

### Module Layout

- **__init__.py**: Exports the public API functions, models, and package metadata
- **core.py**: Contains all implementation code, including public API functions and private helper functions
- **models.py**: Contains Pydantic models that represent the structure of weather data

## Data Flow

The basic flow of data through the package is:

1. User calls `get_weather()` with parameters
2. Parameters are validated
3. If mock mode is enabled, mock data is returned
4. URL is constructed using `_build_url()`
5. Cache is checked using `_get_from_cache()`
6. If data is not in cache, HTTP request is made
7. Response is processed
   - JSON responses are parsed and converted to Pydantic models
   - Text responses are returned as strings
   - PNG responses are returned as bytes
8. Response is stored in cache using `_add_to_cache()`
9. Data is returned to the user

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
- Output format (JSON, raw_json, text, PNG)
- Moon phase requests
- Language settings

This function is critical because the weather service has different URL formats depending on the type of request.

### 2. Pydantic Models

The package uses Pydantic models to provide structured, type-safe access to JSON weather data:

- `WeatherResponse`: Top-level model representing the complete API response
- `CurrentCondition`: Weather conditions at the current time
- `NearestArea`: Location information about the requested area
- `DailyForecast`: Weather forecast for a specific day 
- `HourlyForecast`: Weather forecast for a specific hour
- `Request`: Information about the API request (query string and location type)
- `Astronomy`: Sunrise, sunset, and moon phase data

These models provide validation, type hints, and structured access to the data.

### 3. Caching System

The caching system consists of:

- A module-level dictionary `_cache` that stores responses
- `_get_from_cache()` function to retrieve cached data
- `_add_to_cache()` function to store new data
- Cache duration setting that controls expiration
- Public `clear_cache()` function to manually clear the cache

The cache uses URLs as keys and stores tuples of `(timestamp, data)` as values. This allows for time-based expiration of cache entries.

### 4. Mock Data System

The mock data system allows for development and testing without making real API calls:

- A module-level flag `_USE_MOCK_DATA` to enable/disable mock mode
- Mock data for all three formats (JSON, text, PNG)
- Public `set_mock_mode()` function to control mock mode
- Per-request control with the `use_mock` parameter

Mock data follows the same structure as real API responses, ensuring that code will work the same with both.

### 5. HTTP Request Handling

HTTP requests are made using the `requests` library. This section of the code:

- Sets appropriate headers (User-Agent)
- Makes the GET request with timeout
- Processes the response based on format (JSON, text, PNG)
- Converts JSON responses to Pydantic models
- Handles various error conditions

### 6. Error Handling

The package uses a consistent approach to error handling:

- No exceptions are raised to the user
- All errors are caught and converted to descriptive error messages
- Error messages are returned as strings that start with "Error:"
- HTTP errors include status codes
- Network errors include details about the failure
- JSON parsing errors include information about the validation failure

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

### Format Selection and Response Processing

The package uses the `format` parameter to determine how to process the response:

```python
if format == "png" or is_png:
    data = response.content  # Return raw bytes for images
elif format == "raw_json":
    data = response.text
    json_data = json.loads(data)
    return json_data  # Return raw Python dictionary
elif format == "json":
    data = response.text
    json_data = json.loads(data)
    weather_response = WeatherResponse.parse_obj(json_data)  # Convert to Pydantic model
    return weather_response
else:
    data = response.text     # Return decoded text
```

The older `is_png` parameter is still supported for backward compatibility.

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

The package was designed with teaching in mind, but it also provides good extensibility:

1. **Data Models**: The Pydantic models can be extended or customized
2. **Mock Data**: Mock data can be modified for different testing scenarios
3. **Additional Weather Services**: Support could be added for other weather APIs
4. **Advanced Caching**: The caching system could be enhanced with persistence
5. **Additional Output Formats**: New formats could be added beyond JSON, text, and PNG

## Dependencies

The package has two external dependencies:

1. **requests**: Used for making HTTP requests to the weather service
   - Chosen for its simplicity and widespread use
   - Well-maintained and reliable

2. **pydantic**: Used for data validation and parsing
   - Provides type safety and validation
   - Makes JSON data easier to work with
   - Excellent integration with IDEs for autocompletion

Both dependencies are widely used and well-maintained, minimizing potential issues.
