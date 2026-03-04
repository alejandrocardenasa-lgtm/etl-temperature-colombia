import pandas as pd

def transform(df: pd.DataFrame):

    df = df.copy()

    # Limpieza de comillas
    df.columns = df.columns.str.replace('"', '', regex=False).str.strip().str.lower()

    # 1) correccion de tipos de datos

    # Convertir fecha a datetime 
    df["fechaobservacion"] = pd.to_datetime(df["fechaobservacion"], errors="coerce")

    # Convertir valores numericos 
    df["valorobservado"] = pd.to_numeric(df["valorobservado"], errors="coerce")
    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")

    print("Datos despues de la validacion:")
    print(df.dtypes)

    # Verificar si quedaron nulos despues de convertir tipos
    print("\nValores nulos despues de convertir tipos:")
    print(df.isnull().sum())


    # 2) Reglas de calidad 

    # Eliminamos registros con coordenadas invalidas (0,0)
    # (Estos eran 15 registros y ademas traian <nil> en departamento/municipio)
    df = df[df["longitud"] != 0].copy()

    # Reemplazamos "<nil>" en zonahidrografica por "UNKNOWN"
    df["zonahidrografica"] = df["zonahidrografica"].replace("<nil>", "UNKNOWN")

    # Por seguridad, eliminamos filas donde la fecha o el valor observado queden invalidos
    df = df[df["fechaobservacion"].notna() & df["valorobservado"].notna()].copy()

   
    # 3) Construccion de dimensiones

    # dim_fecha 
    dim_fecha = (
    df[["fechaobservacion"]]
    .drop_duplicates()
    .rename(columns={"fechaobservacion": "full_fechahora"})
    .sort_values("full_fechahora")
    .reset_index(drop=True)
)

    # Crear atributos de fecha
    dim_fecha["fecha_key"] = dim_fecha["full_fechahora"].dt.strftime("%Y%m%d%H").astype(int)
    dim_fecha["anio"] = dim_fecha["full_fechahora"].dt.year
    dim_fecha["mes"] = dim_fecha["full_fechahora"].dt.month
    dim_fecha["dia"] = dim_fecha["full_fechahora"].dt.day
    dim_fecha["hora"] = dim_fecha["full_fechahora"].dt.hour
    dim_fecha["semana"] = dim_fecha["full_fechahora"].dt.isocalendar().week.astype(int)
    dim_fecha["trimestre"] = dim_fecha["full_fechahora"].dt.quarter

    dim_fecha = dim_fecha.drop_duplicates(subset=["fecha_key"])

    # Orden final
    dim_fecha = dim_fecha[
    ["fecha_key", "full_fechahora", "trimestre", "anio", "mes", "semana", "dia", "hora"]
]

    # dim_estacion
    dim_estacion = (
        df[[
            "codigoestacion",
            "nombreestacion",
            "departamento",
            "municipio",
            "zonahidrografica",
            "latitud",
            "longitud"
        ]]
        .drop_duplicates()
        .sort_values(["codigoestacion"])
        .reset_index(drop=True)
    )

    # Surrogate key
    dim_estacion["estacion_key"] = dim_estacion.index + 1

    # Renombrar columnas a nombres más claros
    dim_estacion = dim_estacion.rename(columns={
        "codigoestacion": "codigo_estacion",
        "nombreestacion": "nombre_estacion",
        "zonahidrografica": "zona_hidrografica"
    })

    dim_estacion = dim_estacion[
        ["estacion_key", "codigo_estacion", "nombre_estacion",
         "departamento", "municipio", "zona_hidrografica", "latitud", "longitud"]
    ]

   # --- Estandarizar descripcion del sensor
    df["descripcionsensor"] = df["descripcionsensor"].replace({
    "TEMPERATURA DEL AIRE A 2 m": "Temp Aire 2 m"
})

    #  dim_sensor
    dim_sensor = (
    df[["codigosensor", "descripcionsensor", "unidadmedida"]]
    .drop_duplicates()  
    .sort_values("codigosensor")
    .reset_index(drop=True)
)

    dim_sensor["sensor_key"] = dim_sensor.index + 1

    dim_sensor = dim_sensor.rename(columns={
    "codigosensor": "codigo_sensor",
    "descripcionsensor": "descripcion_sensor",
    "unidadmedida": "unidad_medida"
})

    dim_sensor = dim_sensor[["sensor_key", "codigo_sensor", "descripcion_sensor", "unidad_medida"]]
    
    # 4) Construccion de fact table
    fact = df[["codigoestacion", "codigosensor", "fechaobservacion", "valorobservado"]].copy()

    # Creamos fecha_key para unir con dim_fecha
    fact["fecha_key"] = fact["fechaobservacion"].dt.strftime("%Y%m%d%H").astype(int)

    # Unimos para obtener surrogate keys
    fact = fact.merge(
        dim_estacion[["estacion_key", "codigo_estacion"]],
        left_on="codigoestacion",
        right_on="codigo_estacion",
        how="left"
    )

    fact = fact.merge(
        dim_sensor[["sensor_key", "codigo_sensor"]],
        left_on="codigosensor",
        right_on="codigo_sensor",
        how="left"
    )

    # Seleccionamos estructura final de la fact
    fact_observaciones_temperatura = fact[
        ["fecha_key", "estacion_key", "sensor_key", "valorobservado"]
    ].rename(columns={"valorobservado": "valor_temperatura"}).copy()

    # Surrogate key para la fact (opcional pero util)
    fact_observaciones_temperatura.insert(
        0, "observacion_key", range(1, len(fact_observaciones_temperatura) + 1)
    )

    # Validacion final, que no nos queden keys nulas
    print("\nNulos en la fact final:")
    print(fact_observaciones_temperatura.isnull().sum())

    return dim_fecha, dim_estacion, dim_sensor, fact_observaciones_temperatura