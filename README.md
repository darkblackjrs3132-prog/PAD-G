# PAD-G — Plataforma de Análisis Delictivo Geoespacial

MVP funcional sin módulo de pruebas automatizadas.

## Incluye
- React + Leaflet
- FastAPI
- PostgreSQL + PostGIS
- ETL en Python/Pandas
- Filtros por fecha, delito y alcaldía
- Marcadores y detalle de incidente
- Mapa de calor
- Estadísticas
- GeoJSON

## Opción recomendada: ejecutar con Docker Desktop

1. Instala Docker Desktop.
2. Abre la carpeta `PAD-G` en Visual Studio Code.
3. Abre Terminal > New Terminal.
4. Ejecuta:

```bash
docker compose up --build
```

5. Abre:
- Plataforma: http://localhost:5173
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

Para detener:

```bash
docker compose down
```

Si cambiaste el SQL inicial y quieres recrear la BD:

```bash
docker compose down -v
docker compose up --build
```

## Ejecutar el ETL de ejemplo
Con los contenedores levantados:

```bash
docker compose exec backend python /app/etl/run_etl.py /app/etl/sample_data/muestra_delitos.csv
```

Luego recarga http://localhost:5173.

## Subir tus datos
El CSV debe usar estas columnas:

```text
fecha,hora,delito,categoria,alcaldia,colonia,descripcion,latitud,longitud
```

## Estructura

```text
PAD-G/
├── backend/        FastAPI / Python
├── frontend/       React / Leaflet
├── database/       PostgreSQL / PostGIS
├── etl/            Carga y limpieza CSV
├── docker-compose.yml
├── .env.example
└── README.md
```

## GitHub

