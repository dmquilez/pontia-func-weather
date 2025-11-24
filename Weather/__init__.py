import json
import logging

import azure.functions as func

from weather_service import CityNotFoundError, WeatherService, WeatherServiceError

logger = logging.getLogger("weather")
weather_service = WeatherService()


def main(req: func.HttpRequest) -> func.HttpResponse:
    city = (req.params.get("city") or "").strip()
    if not city:
        try:
            body = req.get_json()
            city = (body.get("city") or "").strip()
        except ValueError:
            city = ""

    if not city:
        return func.HttpResponse(
            body=json.dumps(
                {"error": "Debe indicar el parámetro 'city'.", "code": "missing_city"},
                ensure_ascii=False,
            ),
            status_code=400,
            mimetype="application/json",
        )

    try:
        payload = weather_service.get_weather(city)
        logger.info("Weather data fetched for %s", payload["city"]["name"])
        return func.HttpResponse(
            body=json.dumps(payload, ensure_ascii=False),
            status_code=200,
            mimetype="application/json",
        )
    except CityNotFoundError as exc:
        logger.warning("Ciudad no encontrada: %s", exc)
        return func.HttpResponse(
            body=json.dumps(
                {"error": str(exc), "code": "city_not_found"}, ensure_ascii=False
            ),
            status_code=404,
            mimetype="application/json",
        )
    except WeatherServiceError as exc:
        logger.error("Fallo consultando Open-Meteo: %s", exc)
        return func.HttpResponse(
            body=json.dumps(
                {
                    "error": "No se pudo obtener la climatología en este momento.",
                    "code": "upstream_error",
                },
                ensure_ascii=False,
            ),
            status_code=502,
            mimetype="application/json",
        )
