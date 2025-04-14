# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2025-04-14

### Added
- Added automatic fallback to mock data when encountering 503 rate limit errors for JSON requests
- Added automatic fallback to mock data when JSON parsing fails
- Improved educational experience by providing mock responses instead of error messages during API rate limiting

## [0.2.1] - 2025-04-14

### Changed
- Documentation updates for the raw_json format
- Minor code improvements for raw_json handling

## [0.2.0] - 2025-04-14

### Added
- Added "raw_json" format option for retrieving JSON data as a Python dictionary without Pydantic model conversion
- Updated Python version requirement from 3.7 to 3.10

### Changed
- Enhanced caching implementation to properly handle different format conversions
- Improved mock data handling for raw_json format
- Updated examples to demonstrate the new format option

## [0.1.2] - 2025-12-05

### Changed
- Renamed package from simple-weather to fetch-my-weather
- Updated all documentation and code references to reflect the new name
- Fixed GitHub repository URLs in package metadata

## [0.1.1] - 2025-12-05

### Added
- Comprehensive MkDocs documentation site published to GitHub Pages
- Collection of mini-projects organized by difficulty level (beginner, intermediate, advanced)
- Complete Weather Game World Generator implementation
- Makefile commands for documentation (docs-serve, docs-build, docs-deploy)

### Changed
- Improved README with direct links to documentation sections
- Consolidated package configuration in pyproject.toml (removed setup.cfg)
- Enhanced code formatting and organization

## [0.1.0] - 2025-12-04

### Added
- Initial release of simple-weather package
- Core functionality for fetching weather data from wttr.in
- Support for different location formats (city, airport, coordinates)
- Language and units customization
- Moon phase information
- PNG image output
- Built-in caching mechanism
- User-friendly error handling
- Basic documentation and examples