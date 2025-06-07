from airflow.models import DagBag


def test_dag_loaded():
    dag_bag = DagBag()
    dag = dag_bag.get_dag("openweather_to_gcs")
    assert dag is not None
    assert dag.dag_id == "openweather_to_gcs"
    assert len(dag.tasks) == 3
