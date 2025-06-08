from dags.api_to_gcs import openweather_to_gcs


def test_dag_structure():
    dag = openweather_to_gcs()
    assert dag.dag_id == "openweather_to_gcs"
    assert len(dag.tasks) == 3
