---

# ETL Pipeline – Observaciones de Temperatura en Colombia

## Descripción del Proyecto

Este proyecto implementa un **pipeline ETL** para procesar observaciones de temperatura registradas en estaciones meteorológicas de Colombia.

El objetivo es tomar los datos crudos desde un archivo CSV, limpiarlos y transformarlos, y finalmente cargarlos en un **Data Warehouse** utilizando un modelo dimensional tipo **Star Schema**.

El pipeline fue desarrollado usando **Python, Pandas y MySQL**.

---

# Dataset

El dataset contiene observaciones de temperatura registradas en diferentes estaciones meteorológicas del país.

Cada registro incluye información como:

* código de la estación
* código del sensor
* fecha y hora de la observación
* valor observado de temperatura
* información geográfica de la estación

El dataset se encuentra en:

```
data/raw/temperature_observations_colombia.csv
```

---

# Modelo del Data Warehouse

El proyecto utiliza un **modelo estrella (Star Schema)** compuesto por una tabla de hechos y tres tablas de dimensiones.

## Tabla de Hechos

**fact_observaciones_temperatura**

Contiene las observaciones de temperatura registradas.

Columnas principales:

* observacion_key
* fecha_key
* estacion_key
* sensor_key
* valor_temperatura

---

## Tablas de Dimensiones

### dim_fecha

Contiene información temporal derivada de la fecha de observación.

Columnas:

* fecha_key
* full_fechahora
* trimestre
* anio
* mes
* semana
* dia
* hora

---

### dim_estacion

Contiene información de las estaciones meteorológicas.

Columnas:

* estacion_key
* codigo_estacion
* nombre_estacion
* departamento
* municipio
* zona_hidrografica
* latitud
* longitud

---

### dim_sensor

Contiene información del sensor utilizado para la medición.

Columnas:

* sensor_key
* codigo_sensor
* descripcion_sensor
* unidad_medida

---

# Pipeline ETL

El proceso ETL se divide en tres fases principales.

## 1. Extract

En esta etapa se lee el archivo CSV utilizando **Pandas**.

Archivo fuente:

```
data/raw/temperature_observations_colombia.csv
```

---

## 2. Transform

Durante la fase de transformación se realizan varias operaciones:

* limpieza de nombres de columnas
* validación de tipos de datos
* eliminación de registros inválidos
* manejo de valores faltantes
* creación de atributos de tiempo
* generación de claves sustitutas
* construcción de las tablas de dimensiones
* creación de la tabla de hechos

### Reglas de calidad de datos aplicadas

* eliminación de registros con coordenadas inválidas (0,0)
* reemplazo de valores `<nil>` en `zonahidrografica`
* eliminación de registros con fechas o valores de temperatura inválidos

---

## 3. Load

Los datos transformados se cargan en un **Data Warehouse en MySQL**.

Ejemplo de conexión:

```
mysql+pymysql://root:root@localhost/dw_temperatura
```

Las tablas se cargan utilizando la función **`to_sql()` de Pandas**.

---

# Estructura del Proyecto

```
ETL_ODS
│
├── etl
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── logs.py
│   └── main.py
│
├── data
│   ├── raw
│   └── processed
│
├── diagrams
│
├── notebooks
│
├── logs
│
└── sql
    └── create_tables.sql
```

---

# Sistema de Logs

El pipeline incluye un sistema simple de **logs** que registra la ejecución de cada fase del ETL.

Ejemplo de registro:

```
ETL process started
Extract phase started
Extract phase completed
Transform phase started
Transform phase completed
Load phase started
Load phase completed
ETL process finished
```

Los logs se guardan en:

```
logs/etl.log
```

---

# Cómo Ejecutar el Pipeline

1. Asegurarse de que **MySQL esté corriendo**.

2. Crear las tablas del Data Warehouse usando:

```
sql/create_tables.sql
```

3. Ejecutar el pipeline ETL:

```
python3 etl/main.py
```

---

# Tecnologías Utilizadas

* Python
* Pandas
* SQLAlchemy
* MySQL
* VS Code

---

# Autor

GonoAlejo

