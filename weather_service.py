from __future__ import annotations

import requests


class WeatherServiceError(Exception):
    """Error genérico al consultar Open-Meteo."""


class CityNotFoundError(WeatherServiceError):
    """La ciudad solicitada no figura en la geocodificación."""


class WeatherService:
    _GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    _FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout_seconds: float = 10.0) -> None:
        self._session = requests.Session()
        self._timeout = timeout_seconds

    def get_weather(self, city: str, language: str = "es") -> dict:
        location = self._resolve_city(city.strip(), language)
        forecast = self._fetch_forecast(location)
        return {"city": location, "forecast": forecast}

    def _resolve_city(self, city: str, language: str) -> dict:
        try:
            response = self._session.get(
                self._GEOCODING_URL,
                params={"name": city, "count": 1, "language": language, "format": "json"},
                timeout=self._timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise WeatherServiceError("Error al resolver la ciudad") from exc

        payload = response.json()
        results = payload.get("results") or []
        if not results:
            raise CityNotFoundError(f"No se encontró la ciudad '{city}'")

        top_hit = results[0]
        return {
            "name": top_hit.get("name"),
            "country": top_hit.get("country"),
            "latitude": top_hit["latitude"],
            "longitude": top_hit["longitude"],
            "timezone": top_hit.get("timezone"),
        }

    def _fetch_forecast(self, location: dict) -> dict:
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "timezone": location.get("timezone") or "auto",
            "current": ",".join(
                [
                    "temperature_2m",
                    "apparent_temperature",
                    "pressure_msl",
                    "relative_humidity_2m",
                    "wind_speed_10m",
                    "wind_direction_10m",
                ]
            ),
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "precipitation",
                    "rain",
                    "showers",
                    "snowfall",
                    "cloud_cover",
                    "visibility",
                    "wind_speed_10m",
                    "pressure_msl",
                ]
            ),
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "apparent_temperature_max",
                    "apparent_temperature_min",
                    "sunrise",
                    "sunset",
                    "precipitation_sum",
                    "rain_sum",
                    "snowfall_sum",
                    "windspeed_10m_max",
                ]
            ),
        }
        try:
            response = self._session.get(self._FORECAST_URL, params=params, timeout=self._timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise WeatherServiceError("Error al obtener la climatología") from exc

        return response.json()
