from extract import extract
from transform import transform
from load import load
from logs import log_progress
from sqlalchemy import create_engine

def main():

    log_progress("ETL process started")

    # --- Extract ---
    log_progress("Extract phase started")

    file_path = "data/raw/temperature_observations_colombia.csv"
    df = extract(file_path)

    log_progress("Extract phase completed")

    # --- Transform ---
    log_progress("Transform phase started")

    dim_fecha, dim_estacion, dim_sensor, fact = transform(df)

    log_progress("Transform phase completed")

    # --- Load ---
    log_progress("Load phase started")

    engine = create_engine("mysql+pymysql://root:root@localhost/dw_temperatura")

    load(engine, dim_fecha, dim_estacion, dim_sensor, fact)

    log_progress("Load phase completed")

    log_progress("ETL process finished")


if __name__ == "__main__":
    main()