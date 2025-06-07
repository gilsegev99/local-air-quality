import pandas as pd
from dags.openweather_dag import openweather_to_gcs


def test_convert_to_pq(tmp_path, monkeypatch):
    dag = openweather_to_gcs()
    convert_task = dag.get_task("convert_to_pq")

    monkeypatch.setenv("AIRFLOW_HOME", str(tmp_path))
    df = pd.DataFrame({"a": [1, 2, 3]})
    filenames = ["testfile"]
    objects = ([df], filenames)

    file_paths = convert_task.python_callable(objects)
    assert len(file_paths) == 1
    assert file_paths[0].endswith(".parquet")
