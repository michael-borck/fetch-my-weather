# Design Philosophy of fetch-my-weather

This document explains the design decisions behind the `fetch-my-weather` package, focusing on educational principles, simplicity, and accessibility.

## Core Design Principles

### 1. Education First

The entire package was designed with education as the primary goal. All design decisions prioritize teaching value over advanced features or optimal performance. This means:

- Code is clearly structured and well-documented
- Functions have descriptive names
- Complex operations are broken down into smaller steps
- Implementation details are visible and understandable

### 2. Beginner Accessibility

The API is intentionally designed to be approachable for beginners:

- A single main function (`get_weather()`) handles all functionality
- Parameters have sensible defaults
- Return values are simple (strings or bytes)
- Error handling avoids exceptions in favor of descriptive messages

### 3. Minimalism

The package follows a minimalist approach:

- Small codebase (only two files)
- Single external dependency (requests library)
- Focused functionality with no feature bloat
- Simple data structures

### 4. Practical Learning

While simplified, the package implements real-world programming practices:

- Proper API handling with parameter encoding
- Effective caching for performance
- HTTP request management
- Content type handling
- User-Agent configuration

## Design Decisions

### Why a Single Function API?

The main API consists of a single function with multiple parameters rather than separate functions for different features:

```python
get_weather(location="", units="", view_options="", lang=None,
            is_png=False, png_options="", is_moon=False,
            moon_date=None, moon_location_hint=None)
```

**Rationale:**
- Easier to learn (one function vs. many)
- Parameters naturally group related options
- Consistent with the underlying API
- Reduces cognitive load for beginners

### Why Return Strings, Not Objects?

Unlike many modern API wrappers, `fetch-my-weather` returns plain text strings or raw bytes instead of parsed data structures.

**Rationale:**
- Output is immediately useful without further processing
- Beginners can see the actual data format
- No need to learn complex object models
- Matches the console-oriented nature of the weather service

### Why No Exceptions?

The package never raises exceptions to the caller, instead returning error messages as strings.

**Rationale:**
- Exception handling is often confusing for beginners
- Pattern-based error checking (`if result.startswith("Error:")`) is easy to understand
- Consistent with the string-based return values
- Simpler control flow in user code

### Why In-Memory Caching?

The package uses a simple dictionary-based in-memory cache rather than a more sophisticated caching system.

**Rationale:**
- Transparent implementation that can be easily understood
- No external dependencies for caching
- Sufficient for educational purposes
- Demonstrates basic cache concepts (storage, expiration, lookup)

### Why URL Construction?

Significant code is dedicated to URL construction rather than using a more abstracted approach.

**Rationale:**
- Shows how API endpoints are constructed
- Demonstrates URL encoding concepts
- Provides insight into query parameter formatting
- Reveals the differences between API formats (text vs. PNG, etc.)

## Educational Value

Each component of the package offers specific educational opportunities:

### URL Construction
- Learning about URL structure
- Query parameter formatting
- URL encoding (handling spaces, special characters)
- Differences between path parameters and query parameters

### Caching
- Basic caching concepts
- Time-based expiration
- Memory management
- Performance optimization

### HTTP Requests
- Making network requests
- Setting headers
- Handling different content types
- Understanding status codes

### Parameter Handling
- Input validation
- Optional parameters with defaults
- Parameter combining and formatting

## Comparisons with Alternatives

The design of `fetch-my-weather` differs from many modern API wrappers and weather libraries:

### Compared to Type-Safe, Model-Based Wrappers (like existing pywttr):
- Simpler return types (strings vs. nested objects)
- Fewer dependencies (no need for Pydantic, etc.)
- More educational visibility into raw data
- Less code to understand for beginners

### Compared to Full-Featured Weather Libraries:
- More focused functionality
- Lighter weight
- Lower conceptual overhead
- More suited to teaching basic API concepts

## Future Design Considerations

While maintaining the educational focus, future versions might consider:

1. **Optional Structured Data**: Adding an optional parameter to return structured data for advanced users

2. **More Backend Services**: Supporting additional weather data sources while maintaining the same simple interface

3. **Enhanced Educational Resources**: Adding more inline documentation focused on teaching concepts

4. **Interactive Examples**: Providing Jupyter notebook examples that walk through each feature

## Conclusion

The design of `fetch-my-weather` deliberately prioritizes educational value, beginner accessibility, and conceptual clarity over advanced features, optimal performance, or industrial robustness. This makes it an ideal tool for teaching basic concepts of API interaction, network requests, and data handling in Python.
