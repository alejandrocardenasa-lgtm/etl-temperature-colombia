---

# ETL Pipeline – Observaciones de Temperatura en Colombia

## Descripción del Proyecto

Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** para procesar observaciones de temperatura registradas en estaciones meteorológicas de Colombia.

El objetivo es tomar los datos crudos desde un archivo CSV, limpiarlos y transformarlos, y finalmente cargarlos en un **Data Warehouse** utilizando un modelo dimensional tipo **Star Schema**.

El pipeline fue desarrollado utilizando **Python, Pandas y MySQL**, permitiendo organizar los datos de forma estructurada para facilitar su análisis posterior.

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

# Grain del Modelo

El **grain** del modelo define el nivel de detalle que representa cada fila en la tabla de hechos.

En este proyecto, **una fila de la tabla de hechos representa una medición de temperatura registrada en una estación meteorológica en una fecha y hora específica**.

Es decir, cada registro corresponde a:

* una estación meteorológica
* un sensor
* una fecha y hora de observación
* el valor de temperatura medido

Este nivel de detalle permite realizar análisis a diferentes niveles de agregación, por ejemplo:

* temperatura promedio por estación
* temperatura promedio por mes o año
* comparaciones entre estaciones o regiones

---

# Modelo del Data Warehouse

El proyecto utiliza un **modelo dimensional en esquema estrella (Star Schema)** compuesto por una tabla de hechos y tres tablas de dimensiones.

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

# Justificación del Modelo Dimensional

El modelo dimensional fue diseñado utilizando un **esquema en estrella (Star Schema)**, donde la tabla de hechos **fact_observaciones_temperatura** almacena las mediciones de temperatura como el evento central del análisis.

Esta tabla contiene las **llaves foráneas hacia las dimensiones** y la medida principal **valor_temperatura**, manteniendo el enfoque en el dato cuantitativo que se desea analizar.

Las dimensiones **dim_fecha**, **dim_estacion** y **dim_sensor** almacenan la información descriptiva asociada a cada medición.

La dimensión **dim_fecha** permite realizar análisis temporales por:

* año
* trimestre
* mes
* semana
* día
* hora

La dimensión **dim_estacion** concentra los atributos geográficos y descriptivos de cada estación meteorológica, como el departamento, municipio y zona hidrográfica, evitando redundancia en la tabla de hechos.

Por su parte, la dimensión **dim_sensor** almacena la información relacionada con el tipo de sensor utilizado y su unidad de medida.

Este diseño permite organizar la información de forma eficiente, facilitando consultas analíticas y reduciendo la duplicación de datos.

---
# EDA (Exploratory Data Analysis) 

Antes de transformar y cargar los datos, se realizó una exploración rápida para entender la estructura del dataset y validar calidad:

1) Estructura y tipos de datos

Se revisaron los tipos de datos de las columnas principales. En general, el dataset trae:

codigoestacion y codigosensor como enteros

fechaobservacion como fecha/hora (datetime)

valorobservado como numérico (float)

columnas descriptivas como nombreestacion, departamento, municipio, zonahidrografica como texto

coordenadas latitud y longitud como numéricos

Esto permitió convertir correctamente los campos antes de construir el modelo dimensional.

2) Valores nulos

Después de convertir tipos (fechaobservacion a datetime y variables numéricas a numeric), se validó que no quedaran nulos por errores de conversión.
Además, se filtraron registros donde fechaobservacion o valorobservado quedaran inválidos (nulos), ya que estos campos son claves para el análisis.

3) Reglas de calidad aplicadas

Durante el análisis se identificaron problemas puntuales de calidad, por lo que se aplicaron reglas simples:

Se eliminaron registros con coordenadas inválidas (0,0) (por ejemplo, longitud igual a 0), ya que no representan una ubicación real de estación.

Se reemplazó el valor <nil> en zonahidrografica por "UNKNOWN" para mantener consistencia en la dimensión.

Se estandarizó la descripción del sensor cuando aparecía con variaciones (por ejemplo: "TEMPERATURA DEL AIRE A 2 m" → "Temp Aire 2 m").

4) Resultado final del modelo (después del ETL)

Luego de ejecutar el pipeline completo (Transform + Load), el Data Warehouse quedó poblado con:

dim_fecha: 33,528 registros

dim_estacion: 502 registros

dim_sensor: 1 registro

fact_observaciones_temperatura: 49,992 registros

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
## Indicadores Clave de Desempeño (KPIs) para Análisis Climático

A partir de los datos almacenados en el Data Warehouse se pueden construir diferentes indicadores que permitan analizar el comportamiento de la temperatura y su relación con el cambio climático.

Estos indicadores transforman las observaciones de temperatura en información útil para el análisis climático y la toma de decisiones.

1. Índice de Calentamiento Anual

Descripción:
Analiza la temperatura promedio por año utilizando las observaciones almacenadas en la tabla de hechos.

Objetivo:
Identificar si existe una tendencia de incremento de temperatura a lo largo del tiempo.

Aplicación:
Este indicador permite observar patrones de calentamiento que pueden ser utilizados como referencia para estudios climáticos o políticas de adaptación.

2. Frecuencia de Días de Calor Crítico

Descripción:
Cuenta el número de registros donde la temperatura supera los 30°C.

Objetivo:
Medir la frecuencia de eventos de calor extremo dentro del dataset.

Aplicación:
Este indicador ayuda a analizar el aumento de temperaturas extremas que pueden afectar la salud humana, los ecosistemas y la estabilidad ambiental.

3. Mapa de Vulnerabilidad Térmica por Municipio

Descripción:
Visualización geográfica basada en latitud y longitud de las estaciones meteorológicas.

Objetivo:
Identificar municipios o zonas donde se registran temperaturas más altas de manera recurrente.

Aplicación:
Permite detectar áreas con mayor exposición al calor y priorizar estrategias de mitigación o adaptación climática.

4. Estrés Térmico por Zona Hidrográfica

Descripción:
Analiza las temperaturas máximas agrupadas por zonas hidrográficas.

Objetivo:
Evaluar la presión térmica sobre los ecosistemas y recursos hídricos.

Aplicación:
Puede utilizarse para estudiar el impacto del calor extremo en cuerpos de agua y ecosistemas asociados.

5. Top 10 Municipios con Temperaturas Más Altas

Descripción:
Ranking de los municipios que registran los valores máximos de temperatura dentro del dataset.

Objetivo:
Identificar las ubicaciones con mayores registros de temperatura.

Aplicación:
Este indicador permite detectar zonas con mayor riesgo climático y facilita la priorización de medidas de monitoreo o prevención.

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
* MySQL
* PowerBi

---

# Autor

GonoAlejo

---

