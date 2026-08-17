from datetime import date
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection
from app.services import obtener_incidentes, incidentes_a_geojson, obtener_estadisticas

app = FastAPI(title="PAD-G API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

def validar_rango(fi, ff):
    if fi and ff and fi > ff:
        raise HTTPException(422, "fecha_inicio no puede ser posterior a fecha_fin")

@app.get("/")
def root(): return {"sistema": "PAD-G", "estado": "operativo"}

@app.get("/api/health")
def health():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 AS ok"); cur.fetchone()
    return {"status": "ok", "database": "connected"}

@app.get("/api/alcaldias")
def alcaldias():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT DISTINCT alcaldia FROM incidentes ORDER BY alcaldia")
        return [r["alcaldia"] for r in cur.fetchall()]

@app.get("/api/tipos-delito")
def tipos_delito():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT DISTINCT delito FROM incidentes ORDER BY delito")
        return [r["delito"] for r in cur.fetchall()]

@app.get("/api/incidentes")
def incidentes(fecha_inicio: date|None=Query(None), fecha_fin: date|None=Query(None), delito: str|None=Query(None), alcaldia: str|None=Query(None)):
    validar_rango(fecha_inicio, fecha_fin)
    return incidentes_a_geojson(obtener_incidentes(fecha_inicio, fecha_fin, delito, alcaldia))

@app.get("/api/incidentes/{id_incidente}")
def incidente_detalle(id_incidente: int):
    sql = """SELECT id_incidente,fecha,hora,delito,categoria,alcaldia,colonia,descripcion,
             ST_X(geom) longitud, ST_Y(geom) latitud FROM incidentes WHERE id_incidente=%s"""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, [id_incidente]); row = cur.fetchone()
    if not row: raise HTTPException(404, "Incidente no encontrado")
    row["fecha"] = row["fecha"].isoformat(); row["hora"] = str(row["hora"]) if row["hora"] else None
    return row

@app.get("/api/estadisticas")
def estadisticas(fecha_inicio: date|None=Query(None), fecha_fin: date|None=Query(None), delito: str|None=Query(None), alcaldia: str|None=Query(None)):
    validar_rango(fecha_inicio, fecha_fin)
    return obtener_estadisticas(fecha_inicio, fecha_fin, delito, alcaldia)

@app.get("/api/heatmap")
def heatmap(fecha_inicio: date|None=Query(None), fecha_fin: date|None=Query(None), delito: str|None=Query(None), alcaldia: str|None=Query(None)):
    validar_rango(fecha_inicio, fecha_fin)
    rows = obtener_incidentes(fecha_inicio, fecha_fin, delito, alcaldia)
    return [{"lat":r["latitud"], "lng":r["longitud"], "intensity":1} for r in rows]
