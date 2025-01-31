import pytest
from main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_items():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b'<h1>Hardware Company</h1>' in response.data

def test_add_document():
    client = app.test_client()
    response = client.get("/new-item")
    assert response.status_code == 200

def test_query1():
    client = app.test_client()
    response = client.get("/query1")
    assert response.status_code == 200
    assert b'Query1' in response.data

def test_query2():
    client = app.test_client()
    response = client.get("/query2")
    assert response.status_code == 200

def test_query3():
    client = app.test_client()
    response = client.get("/query3")
    assert response.status_code == 200

def test_query4():
    client = app.test_client()
    response = client.get("/query4")
    assert response.status_code == 200

def test_query5():
    client = app.test_client()
    response = client.get("/query5")
    assert response.status_code == 200

def test_query8():
    client = app.test_client()
    response = client.get("/query8")
    assert response.status_code == 200

def test_query9():
    client = app.test_client()
    response = client.get("/query9")
    assert response.status_code == 200

def test_query10():
    client = app.test_client()
    response = client.get("/query10")
    assert response.status_code == 200

def test_query11():
    client = app.test_client()
    response = client.get("/query11")
    assert response.status_code == 200

def test_query12():
    client = app.test_client()
    response = client.get("/query12")
    assert response.status_code == 200

def test_query13():
    client = app.test_client()
    response = client.get("/query13")
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data[0]["_id"] == "AMD Ryzen 5 5600X"

def test_query14():
    client = app.test_client()
    response = client.get("/query14")
    assert response.status_code == 200

