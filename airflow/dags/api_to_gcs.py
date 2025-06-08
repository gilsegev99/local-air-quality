import logging
import os
from datetime import datetime, timedelta

import pandas as pd
import pytz
import requests
from airflow.decorators import dag, task
from google.cloud import storage

API_KEY = os.getenv("API_KEY")
GCS_BUCKET = "local-air-quality-bucket"

logger = logging.getLogger(__name__)


def get_current_time():
    # Get current time
    current_time = datetime.now()

    # Convert to UTC time zone
    current_time_utc = datetime.now(pytz.utc)

    # Convert UTC time to Unix time
    unix_time = int(current_time_utc.timestamp())
    print("Current time in local:", current_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    print("Current time in UTC:", current_time_utc.strftime("%Y-%m-%d %H:%M:%S %Z"))
    print("Unix time:", unix_time)
    return unix_time


def datetime_to_utcunix(datetime: datetime):
    unix_time = int(datetime.timestamp())
    return unix_time


def format_response(coords, body):
    components = body["components"]
    data = {
        "lon": str(coords["lon"]),
        "lat": str(coords["lat"]),
        "aqi": str(body["main"]["aqi"]),
        "co": float(components["co"]),
        "no": float(components["no"]),
        "no2": float(components["no2"]),
        "o3": float(components["o3"]),
        "so2": float(components["so2"]),
        "pm2_5": float(components["pm2_5"]),
        "pm10": float(components["pm10"]),
        "nh3": float(components["nh3"]),
        "time": str(body["dt"]),
    }
    return data


def get_location_list():
    return pd.read_csv(f"{AIRFLOW_HOME}/data/location_list.csv")


# Define DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 4, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

NOW = get_current_time()
# API Data available from 2020/11/27
START = datetime_to_utcunix(datetime(2020, 12, 1))
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


@dag(default_args=default_args, schedule=None, catchup=False)
def openweather_to_gcs():

    @task
    def fetch_api_data(start, end, api_key, **kwargs):
        dfs = []
        files = []

        for index, row in get_location_list().iterrows():
            lat = row["Latitude"]
            lon = row["Longitude"]
            location = row["Location"]

            api_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history? \
                        lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"

            try:
                logger.info(f"Requesting data for {location}")
                logger.info(f"Using API Key: {api_key}")
                response = requests.get(api_url)
                response.raise_for_status()

                data = response.json()

                if "list" not in data:
                    logger.warning(f"Data unavailable for {location}")

                df = pd.DataFrame(
                    [
                        format_response(data["coord"], datapoint)
                        for datapoint in data["list"]
                    ]
                )
                dfs.append(df)

                file_name = f"pollution_data_{location}_{start}-{end}"
                files.append(file_name)

                logger.info(f"Successfully retrieved {len(df)} records for {location}")

            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP error for {location}: {http_err}")

        return dfs, files

    @task
    def convert_to_pq(objects):
        dataframes, filenames = objects
        file_paths = []

        if len(dataframes) != len(filenames):
            return None

        output_dir = os.path.join(AIRFLOW_HOME, "tmp")
        os.makedirs(output_dir, exist_ok=True)

        for i in range(len(dataframes)):
            file_path = os.path.join(output_dir, f"{filenames[i]}.parquet")
            dataframes[i].to_parquet(file_path, engine="pyarrow")
            file_paths.append(file_path)

        return file_paths

    @task
    def upload_to_gcs(file_paths, **kwargs):
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)

        for file_path in file_paths:

            blob = bucket.blob(os.path.basename(file_path))

            blob.upload_from_filename(file_path)
            os.remove(file_path)  # Clean up

    # Set task dependencies

    objects = fetch_api_data(START, NOW, API_KEY)
    file_paths = convert_to_pq(objects)
    upload_to_gcs(file_paths)


extract_data = openweather_to_gcs()
