import os
from airflow.decorators import dag, task

from datetime import datetime, timedelta
import pytz
import requests
import pandas as pd
import pyarrow.parquet as pq
from google.cloud import storage


API_KEY = os.getenv("API_KEY")
GCS_BUCKET = "local-air-quality-bucket"

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
    components = body['components']
    data = {
        'lon': str(coords['lon']),
        'lat': str(coords['lat']),
        'aqi': str(body['main']['aqi']),
        'co': float(components['co']),
        'no': float(components['no']),
        'no2': float(components['no2']),
        'o3': float(components['o3']),
        'so2': float(components['so2']),
        'pm2_5': float(components['pm2_5']),
        'pm10': float(components['pm10']),
        'nh3': float(components['nh3']),
        'time': str(body['dt'])
    }
    return data

# Define DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 4, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

NOW = get_current_time()
START = datetime_to_utcunix(datetime(2020, 1, 1))
LOCATION_LIST = pd.read_csv("/home/src/location_list.csv")

@dag(
    default_args=default_args,
    schedule_interval="@daily",
)
def openweather_to_gcs():

    @task
    def fetch_api_data(start_date, end_date, api_key, **kwargs):
        dfs = []
        files = []

        for index, row in LOCATION_LIST.iterrows():
            lat = row['Latitude']
            lon = row['Longitude']
            api_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start_date}&end={end_date}&appid={api_key}"

            response = requests.get(api_url)
            data = response.json()

            df = pd.DataFrame([format_response(data['coord'], datapoint) for datapoint in data['list']])
            dfs.append(df)

            file_name = f"pollution_data_{row['Location']}_{start_date}-{end_date}"
            files.append(file_name)

        return dfs, files


    @task
    def convert_to_pq(dataframes, filenames):
        file_paths = []

        # data, files = fetch_api_data()

        if len(dataframes) != len(files):
            return None

        for i in len(dataframes):
            file_path = f"tmp/{files[i]}.parquet"
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

    dataframes, filenames = fetch_api_data(START, NOW, API_KEY)
    file_paths = convert_to_pq(dataframes,filenames)
    upload_to_gcs(file_paths)

extract_data = openweather_to_gcs()  

