"""
Pydantic models for the wttr.in API responses.

These models define the structure of the JSON data returned by the wttr.in API,
providing type safety, validation, and easier access to weather data.
"""

from typing import List, Optional, Any, Dict, Union

from pydantic import BaseModel, Field


class ResponseMetadata(BaseModel):
    """Metadata about the response from fetch-my-weather."""
    
    # Source of data
    is_real_data: bool = True  # Whether this is real data from the API
    is_cached: bool = False  # Whether this came from cache
    is_mock: bool = False  # Whether this is fallback mock data
    
    # Error information
    status_code: Optional[int] = None  # HTTP status code if available
    error_type: Optional[str] = None  # Type of error if any (e.g., "JSONDecodeError")
    error_message: Optional[str] = None  # Detailed error message if any
    
    # Request information
    url: Optional[str] = None  # URL that was requested
    timestamp: Optional[float] = None  # When the request was made


class WeatherDesc(BaseModel):
    """Weather description model."""

    value: str


class WeatherIconUrl(BaseModel):
    """Weather icon URL model."""

    value: str


class Astronomy(BaseModel):
    """Astronomy information including sunrise, sunset, moonrise, moonset, etc."""

    moon_illumination: Optional[str] = None
    moon_phase: Optional[str] = None
    moonrise: Optional[str] = None
    moonset: Optional[str] = None
    sunrise: Optional[str] = None
    sunset: Optional[str] = None


class AreaName(BaseModel):
    """Area name model."""

    value: str


class Country(BaseModel):
    """Country model."""

    value: str


class Region(BaseModel):
    """Region model."""

    value: str


class HourlyForecast(BaseModel):
    """Hourly weather forecast data."""

    DewPointC: Optional[str] = None
    DewPointF: Optional[str] = None
    FeelsLikeC: Optional[str] = None
    FeelsLikeF: Optional[str] = None
    HeatIndexC: Optional[str] = None
    HeatIndexF: Optional[str] = None
    WindChillC: Optional[str] = None
    WindChillF: Optional[str] = None
    WindGustKmph: Optional[str] = None
    WindGustMiles: Optional[str] = None
    chanceoffog: Optional[str] = None
    chanceoffrost: Optional[str] = None
    chanceofhightemp: Optional[str] = None
    chanceofovercast: Optional[str] = None
    chanceofrain: Optional[str] = None
    chanceofremdry: Optional[str] = None
    chanceofsnow: Optional[str] = None
    chanceofsunshine: Optional[str] = None
    chanceofthunder: Optional[str] = None
    chanceofwindy: Optional[str] = None
    cloudcover: Optional[str] = None
    humidity: Optional[str] = None
    precipInches: Optional[str] = None
    precipMM: Optional[str] = None
    pressure: Optional[str] = None
    pressureInches: Optional[str] = None
    tempC: Optional[str] = None
    tempF: Optional[str] = None
    time: Optional[str] = None
    uvIndex: Optional[str] = None
    visibility: Optional[str] = None
    visibilityMiles: Optional[str] = None
    weatherCode: Optional[str] = None
    weatherDesc: List[WeatherDesc] = Field(default_factory=list)
    weatherIconUrl: List[WeatherIconUrl] = Field(default_factory=list)
    winddir16Point: Optional[str] = None
    winddirDegree: Optional[str] = None
    windspeedKmph: Optional[str] = None
    windspeedMiles: Optional[str] = None


class CurrentCondition(BaseModel):
    """Current weather conditions."""

    FeelsLikeC: Optional[str] = None
    FeelsLikeF: Optional[str] = None
    cloudcover: Optional[str] = None
    humidity: Optional[str] = None
    localObsDateTime: Optional[str] = None
    observation_time: Optional[str] = None
    precipInches: Optional[str] = None
    precipMM: Optional[str] = None
    pressure: Optional[str] = None
    pressureInches: Optional[str] = None
    temp_C: Optional[str] = None
    temp_F: Optional[str] = None
    uvIndex: Optional[str] = None
    visibility: Optional[str] = None
    visibilityMiles: Optional[str] = None
    weatherCode: Optional[str] = None
    weatherDesc: List[WeatherDesc] = Field(default_factory=list)
    weatherIconUrl: List[WeatherIconUrl] = Field(default_factory=list)
    winddir16Point: Optional[str] = None
    winddirDegree: Optional[str] = None
    windspeedKmph: Optional[str] = None
    windspeedMiles: Optional[str] = None


class DailyForecast(BaseModel):
    """Daily weather forecast data."""

    astronomy: List[Astronomy] = Field(default_factory=list)
    avgtempC: Optional[str] = None
    avgtempF: Optional[str] = None
    date: Optional[str] = None
    hourly: List[HourlyForecast] = Field(default_factory=list)
    maxtempC: Optional[str] = None
    maxtempF: Optional[str] = None
    mintempC: Optional[str] = None
    mintempF: Optional[str] = None
    sunHour: Optional[str] = None
    totalSnow_cm: Optional[str] = None
    uvIndex: Optional[str] = None


class NearestArea(BaseModel):
    """Information about the nearest area."""

    areaName: List[AreaName] = Field(default_factory=list)
    country: List[Country] = Field(default_factory=list)
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    population: Optional[str] = None
    region: List[Region] = Field(default_factory=list)
    weatherUrl: List[WeatherIconUrl] = Field(default_factory=list)


class Request(BaseModel):
    """Information about the request that was made."""

    query: Optional[str] = None
    type: Optional[str] = None


class WeatherResponse(BaseModel):
    """Complete weather response from wttr.in API."""

    current_condition: List[CurrentCondition] = Field(default_factory=list)
    nearest_area: List[NearestArea] = Field(default_factory=list)
    request: List[Request] = Field(default_factory=list)
    weather: List[DailyForecast] = Field(default_factory=list)
    
    # Metadata for tracking response type and status
    metadata: ResponseMetadata = Field(default_factory=ResponseMetadata)


class ResponseWrapper(BaseModel):
    """Wrapper for any response with metadata."""
    
    data: Any  # The actual response data (text, bytes, dict)
    metadata: ResponseMetadata  # Metadata about the response
