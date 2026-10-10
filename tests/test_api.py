import pytest
from fastapi.testclient import TestClient

from src import api
from src.schema import Measurement
from src.storage import save_to_sqlite


client = TestClient(api.app)


# A tiny set of rows where we already know the answers
def make_rows():
    return [
        Measurement(strain="strain_a", replicate=1, time_h=0.0, od600=0.0),
        Measurement(strain="strain_a", replicate=1, time_h=1.0, od600=1.0),
        Measurement(strain="strain_a", replicate=1, time_h=2.0, od600=1.5),
        Measurement(strain="strain_b", replicate=1, time_h=0.0, od600=0.0),
        Measurement(strain="strain_b", replicate=1, time_h=1.0, od600=0.2),
        Measurement(strain="strain_b", replicate=1, time_h=2.0, od600=0.4),
    ]


@pytest.fixture(autouse=True)
def use_test_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    save_to_sqlite(make_rows(), db_path)
    monkeypatch.setattr(api, "DB_PATH", db_path)


def test_list_strains():
    response = client.get("/strains")
    assert response.status_code == 200
    assert response.json() == {"strains": ["strain_a", "strain_b"]}


def test_strain_summary():
    response = client.get("/strains/strain_a/summary")
    assert response.status_code == 200
    assert response.json()["peak_od"] == 1.5
    assert response.json()["max_growth_rate"] == 1.0


def test_unknown_strain_gives_404():
    response = client.get("/strains/banana/summary")
    assert response.status_code == 404


def test_fastest_strain():
    response = client.get("/fastest-strain")
    assert response.status_code == 200
    assert response.json() == {"fastest_strain": "strain_a"}