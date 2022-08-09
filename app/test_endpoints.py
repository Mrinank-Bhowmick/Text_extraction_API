from http import client
from urllib import response
from app.main import app
from fastapi.testclient import TestClient

client=TestClient(app)        # This is similer to python requests module



def test_get():
    response=client.get("/")
    assert response.status_code==200
    assert "text/html" in response.headers['content-type']


def test_post():
    response=client.post("/")
    assert response.status_code==200
    assert response.headers['content-type'] == "application/json"




