CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS incidentes (
    id_incidente SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME,
    delito VARCHAR(200) NOT NULL,
    categoria VARCHAR(120),
    alcaldia VARCHAR(120) NOT NULL,
    colonia VARCHAR(180),
    descripcion TEXT,
    latitud DOUBLE PRECISION NOT NULL,
    longitud DOUBLE PRECISION NOT NULL,
    geom geometry(Point, 4326) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_incidentes_geom ON incidentes USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_incidentes_fecha ON incidentes (fecha);
CREATE INDEX IF NOT EXISTS idx_incidentes_alcaldia ON incidentes (alcaldia);
CREATE INDEX IF NOT EXISTS idx_incidentes_delito ON incidentes (delito);

INSERT INTO incidentes
(fecha,hora,delito,categoria,alcaldia,colonia,descripcion,latitud,longitud,geom)
VALUES
('2026-01-05','09:30','Robo a transeúnte','Robo','Coyoacán','Del Carmen','Incidente de ejemplo',19.3505,-99.1620,ST_SetSRID(ST_MakePoint(-99.1620,19.3505),4326)),
('2026-01-12','18:15','Robo de vehículo','Robo','Iztapalapa','Santa Martha Acatitla','Incidente de ejemplo',19.3601,-99.0068,ST_SetSRID(ST_MakePoint(-99.0068,19.3601),4326)),
('2026-02-02','14:20','Fraude','Patrimonial','Cuauhtémoc','Centro','Incidente de ejemplo',19.4327,-99.1332,ST_SetSRID(ST_MakePoint(-99.1332,19.4327),4326)),
('2026-02-14','21:10','Lesiones','Integridad física','Gustavo A. Madero','Lindavista','Incidente de ejemplo',19.4969,-99.1260,ST_SetSRID(ST_MakePoint(-99.1260,19.4969),4326)),
('2026-03-03','11:45','Robo a casa habitación','Robo','Benito Juárez','Narvarte','Incidente de ejemplo',19.3898,-99.1542,ST_SetSRID(ST_MakePoint(-99.1542,19.3898),4326)),
('2026-03-18','16:40','Robo a transeúnte','Robo','Coyoacán','Copilco Universidad','Incidente de ejemplo',19.3335,-99.1761,ST_SetSRID(ST_MakePoint(-99.1761,19.3335),4326)),
('2026-04-01','08:05','Robo a transeúnte','Robo','Cuauhtémoc','Roma Norte','Incidente de ejemplo',19.4194,-99.1628,ST_SetSRID(ST_MakePoint(-99.1628,19.4194),4326)),
('2026-04-19','22:30','Robo de vehículo','Robo','Iztapalapa','Constitución de 1917','Incidente de ejemplo',19.3456,-99.0634,ST_SetSRID(ST_MakePoint(-99.0634,19.3456),4326));
