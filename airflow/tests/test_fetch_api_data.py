from unittest.mock import patch

import pandas as pd
from dags.api_to_gcs import openweather_to_gcs


def test_fetch_api_data():
    dag = openweather_to_gcs()
    fetch_task = dag.get_task("fetch_api_data")

    mock_response = {
        "coord": {"lon": 10.0, "lat": -10.0},
        "list": [
            {
                "main": {"aqi": 2},
                "components": {
                    "co": 0.1,
                    "no": 0.2,
                    "no2": 0.3,
                    "o3": 0.4,
                    "so2": 0.5,
                    "pm2_5": 0.6,
                    "pm10": 0.7,
                    "nh3": 0.8,
                },
                "dt": 1234567890,
            }
        ],
    }

    with patch(
        "dags.openweather_dag.LOCATION_LIST",
        new=pd.DataFrame(
            [{"Latitude": 10.0, "Longitude": -10.0, "Location": "TestLocation"}]
        ),
    ), patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        dfs, filenames = fetch_task.python_callable(123, 456, "fake_key")
        assert len(dfs) == 1
        assert len(filenames) == 1

        df = dfs[0]
        assert not df.empty
        assert "co" in df.columns
        assert df.iloc[0]["co"] == 0.1
        assert df.iloc[0]["aqi"] == "2"
        assert df.iloc[0]["lat"] == "-10.0"
