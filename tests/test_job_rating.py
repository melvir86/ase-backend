import pytest
import sqlite3
from flaskr import create_app
import warnings
import json
import requests

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_listJob(client):
    # Prepare a JSON payload for the request

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/listJob?uid=1')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    job = json.loads(response.get_data(as_text=True))
    #print("Booking response")
    #print(booking)

    assert job is not None


def test_driverRating(client):
    # Prepare a JSON payload for the request

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/driverRating?uid=1')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    rating = json.loads(response.get_data(as_text=True))
    

    assert rating is not None
    