from dags.api_to_gcs import format_response


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
