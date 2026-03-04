import os

def load(engine, dim_fecha, dim_estacion, dim_sensor, fact_observaciones_temperatura):

    # Guardar CSV trasnformados, backup 
    os.makedirs("data/processed", exist_ok=True)

    dim_fecha.to_csv("data/processed/dim_fecha.csv", index=False)
    dim_estacion.to_csv("data/processed/dim_estacion.csv", index=False)
    dim_sensor.to_csv("data/processed/dim_sensor.csv", index=False)
    fact_observaciones_temperatura.to_csv("data/processed/fact_observaciones_temperatura.csv", index=False)

    # Cargar dimensiones primero
    dim_fecha.to_sql("dim_fecha", engine, if_exists="append", index=False)
    dim_estacion.to_sql("dim_estacion", engine, if_exists="append", index=False)
    dim_sensor.to_sql("dim_sensor", engine, if_exists="append", index=False)

    # Luego la fact table
    fact_observaciones_temperatura.to_sql(
        "fact_observaciones_temperatura",
        engine,
        if_exists="append",
        index=False
    )
