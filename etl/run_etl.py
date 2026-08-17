import os, sys
import pandas as pd
import psycopg

REQUIRED = ["fecha","hora","delito","categoria","alcaldia","colonia","descripcion","latitud","longitud"]

def conn():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST","db"), port=os.getenv("POSTGRES_PORT","5432"),
        dbname=os.getenv("POSTGRES_DB","padg"), user=os.getenv("POSTGRES_USER","padg_user"),
        password=os.getenv("POSTGRES_PASSWORD","padg_password")
    )

def transformar(df):
    faltantes = [c for c in REQUIRED if c not in df.columns]
    if faltantes: raise ValueError(f"Faltan columnas: {faltantes}")
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")
    df = df.dropna(subset=["fecha","delito","alcaldia","latitud","longitud"])
    df = df[df["latitud"].between(19.0,20.0) & df["longitud"].between(-100.0,-98.0)]
    return df

def cargar(df):
    sql = """INSERT INTO incidentes
    (fecha,hora,delito,categoria,alcaldia,colonia,descripcion,latitud,longitud,geom)
    VALUES (%s,NULLIF(%s,'')::time,%s,%s,%s,%s,%s,%s,%s,ST_SetSRID(ST_MakePoint(%s,%s),4326))"""
    with conn() as c, c.cursor() as cur:
        for _, r in df.iterrows():
            cur.execute(sql,[r["fecha"],str(r["hora"]) if pd.notna(r["hora"]) else "",r["delito"],r["categoria"],r["alcaldia"],r["colonia"],r["descripcion"],float(r["latitud"]),float(r["longitud"]),float(r["longitud"]),float(r["latitud"])])
        c.commit()

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Uso: python run_etl.py archivo.csv"); raise SystemExit(1)
    df = pd.read_csv(sys.argv[1]); print("Leídos:",len(df))
    df = transformar(df); print("Válidos:",len(df))
    cargar(df); print("Carga ETL terminada")
