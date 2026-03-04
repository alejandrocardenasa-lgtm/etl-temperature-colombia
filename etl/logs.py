import datetime
import os

def log_progress(message, log_file="logs/etl.log"):

    os.makedirs("logs", exist_ok=True)

    timestamp_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open(log_file, "a") as f:
        f.write(timestamp + " - " + message + "\n")