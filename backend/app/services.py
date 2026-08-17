from app.database import get_connection

def construir_filtros(fecha_inicio=None, fecha_fin=None, delito=None, alcaldia=None):
    where, params = [], []
    if fecha_inicio:
        where.append("fecha >= %s"); params.append(fecha_inicio)
    if fecha_fin:
        where.append("fecha <= %s"); params.append(fecha_fin)
    if delito:
        where.append("delito = %s"); params.append(delito)
    if alcaldia:
        where.append("alcaldia = %s"); params.append(alcaldia)
    return (" WHERE " + " AND ".join(where) if where else ""), params

def obtener_incidentes(fecha_inicio=None, fecha_fin=None, delito=None, alcaldia=None):
    where, params = construir_filtros(fecha_inicio, fecha_fin, delito, alcaldia)
    sql = f"""
        SELECT id_incidente, fecha, hora, delito, categoria, alcaldia, colonia,
               descripcion, ST_X(geom) AS longitud, ST_Y(geom) AS latitud
        FROM incidentes {where}
        ORDER BY fecha DESC, hora DESC NULLS LAST
        LIMIT 5000
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def incidentes_a_geojson(rows):
    return {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [r["longitud"], r["latitud"]]},
            "properties": {
                "id": r["id_incidente"], "fecha": r["fecha"].isoformat(),
                "hora": str(r["hora"]) if r["hora"] else None,
                "delito": r["delito"], "categoria": r["categoria"],
                "alcaldia": r["alcaldia"], "colonia": r["colonia"],
                "descripcion": r["descripcion"]
            }
        } for r in rows]
    }

def obtener_estadisticas(fecha_inicio=None, fecha_fin=None, delito=None, alcaldia=None):
    where, params = construir_filtros(fecha_inicio, fecha_fin, delito, alcaldia)
    q1 = f"SELECT COUNT(*)::int total_incidentes, COUNT(DISTINCT fecha)::int dias FROM incidentes {where}"
    q2 = f"SELECT delito, COUNT(*)::int total FROM incidentes {where} GROUP BY delito ORDER BY total DESC, delito LIMIT 8"
    q3 = f"SELECT alcaldia, COUNT(*)::int total FROM incidentes {where} GROUP BY alcaldia ORDER BY total DESC, alcaldia LIMIT 8"
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(q1, params); resumen = cur.fetchone()
        cur.execute(q2, params); por_delito = cur.fetchall()
        cur.execute(q3, params); por_alcaldia = cur.fetchall()
    total, dias = resumen["total_incidentes"] or 0, resumen["dias"] or 0
    return {
        "total_incidentes": total,
        "promedio_diario": round(total / dias, 2) if dias else 0,
        "delito_mas_frecuente": por_delito[0]["delito"] if por_delito else None,
        "alcaldia_mayor_incidencia": por_alcaldia[0]["alcaldia"] if por_alcaldia else None,
        "por_delito": por_delito,
        "por_alcaldia": por_alcaldia
    }
