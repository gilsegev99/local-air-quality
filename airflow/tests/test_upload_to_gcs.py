import os
from unittest.mock import MagicMock, patch

from dags.api_to_gcs import openweather_to_gcs


def test_upload_to_gcs(tmp_path):
    test_file = tmp_path / "testfile.parquet"
    test_file.write_text("test content")

    dag = openweather_to_gcs()
    upload_task = dag.get_task("upload_to_gcs")

    with patch("google.cloud.storage.Client") as mock_client:
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob

        upload_task.python_callable([str(test_file)])

        assert mock_bucket.blob.call_count == 1
        assert mock_blob.upload_from_filename.call_count == 1
        mock_client.return_value.bucket.assert_called_with("local-air-quality-bucket")
        assert not os.path.exists(test_file)  # file is deleted
