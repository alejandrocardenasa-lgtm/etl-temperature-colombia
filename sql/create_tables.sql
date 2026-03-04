CREATE DATABASE DW_Temperatura;
USE DW_Temperatura;

# dim_fecha
CREATE TABLE dim_fecha (
  fecha_key INT AUTO_INCREMENT PRIMARY KEY,
  full_fechahora DATETIME NOT NULL,
  trimestre INT,
  anio INT,
  mes INT,
  semana INT,
  dia INT,
  hora INT
);

# dim_estacion
CREATE TABLE dim_estacion (
  estacion_key INT AUTO_INCREMENT PRIMARY KEY,
  codigo_estacion VARCHAR(50),
  nombre_estacion VARCHAR(255),
  departamento VARCHAR(100),
  municipio VARCHAR(100),
  zona_hidrografica VARCHAR(255),
  latitud DECIMAL(10,6),
  longitud DECIMAL(10,6)
);

# dim_sensor
CREATE TABLE dim_sensor (
  sensor_key INT AUTO_INCREMENT PRIMARY KEY,
  codigo_sensor VARCHAR(50),
  descripcion_sensor VARCHAR(255),
  unidad_medida VARCHAR(50)
);

# fact_table
CREATE TABLE fact_observaciones_temperatura (
  observacion_key INT AUTO_INCREMENT PRIMARY KEY,

  fecha_key    INT NOT NULL,
  estacion_key INT NOT NULL,
  sensor_key   INT NOT NULL,

  valor_temperatura DECIMAL(6,2) NOT NULL,

  FOREIGN KEY (fecha_key)    REFERENCES dim_fecha(fecha_key),
  FOREIGN KEY (estacion_key) REFERENCES dim_estacion(estacion_key),
  FOREIGN KEY (sensor_key)   REFERENCES dim_sensor(sensor_key)
);
