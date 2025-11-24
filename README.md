# Azure Function: Weather by City

## Requisitos
- Python 3.11+
- Azure Functions Core Tools v4
- Azure Functions Runtime v4 (Python Programming Model V1)

## Estructura del Proyecto
```
func-weather-pontia/
├── Weather/
│   ├── __init__.py
│   └── function.json
├── weather_service.py
├── host.json
├── requirements.txt
└── .gitignore
```

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución local
```bash
func start
```

## Uso
```bash
curl "http://localhost:7071/api/weather?city=Madrid"
```

Respuesta:
```json
{
  "city": {
    "name": "Madrid",
    "country": "Spain",
    "latitude": 40.4165,
    "longitude": -3.70256,
    "timezone": "Europe/Madrid"
  },
  "forecast": {
    "current": { "...": "..." },
    "hourly": { "...": "..." },
    "daily": { "...": "..." }
  }
}
```

Admite `GET /api/weather?city=<nombre>` o cuerpo JSON `{"city": "..."}`.

## Despliegue
Publica con:
```bash
func azure functionapp publish <nombre-app>
```
