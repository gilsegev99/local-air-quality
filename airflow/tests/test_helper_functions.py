import unittest
from unittest.mock import MagicMock, patch

from dags.api_to_gcs import (
    START,
    format_response,
    get_last_ingestion_timestamp,
    update_last_ingestion_time,
)


def test_format_response_valid():
    coords = {"lon": 10.0, "lat": -10.0}
    body = {
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
        "dt": 11111111,
    }

    result = format_response(coords, body)
    assert result["aqi"] == "2"
    assert result["co"] == 0.1
    assert result["lat"] == "-10.0"


def test_update_last_ingestion_time():

    with patch("google.cloud.bigquery.Client") as mock_client_class:

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        update_last_ingestion_time()

        mock_client.query.assert_called_once()
        mock_client.query.return_value.result.assert_called_once()


class TestGetLastIngestionTimestamp(unittest.TestCase):

    def test_existing_timestamp_returned(self):

        with patch("google.cloud.bigquery.Client") as mock_client_class:

            mock_row = MagicMock()
            mock_row.last_ingested_at = 123456789

            mock_result = [mock_row]

            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            mock_client.query.return_value.result.return_value = mock_result

            returned_value = get_last_ingestion_timestamp()

            self.assertEqual(returned_value, 123456789)

    def test_no_existing_timestamp(self):

        with patch("google.cloud.bigquery.Client") as mock_client_class:

            mock_result = []

            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            mock_client_class.query.return_value.result.return_value = mock_result

            returned_value = get_last_ingestion_timestamp()

            self.assertEqual(returned_value, START)
