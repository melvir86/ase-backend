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

def test_show_cars_success(client):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response = client.get('/api/showCars')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    # Add additional assertions to validate the response data
    assert b'Mazda' in response.data
    assert b'6' in response.data
    assert b'Mazda' in response.data
    assert b'3 Hb' in response.data

def test_bookcar(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    payload = {
        'uid': 6,
        'source': 'Manchester',
        'destination': 'Liverpool'
    }

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/bookcar', json=payload)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    booking = json.loads(response.get_data(as_text=True))
    #print("Booking response")
    #print(booking)

    assert booking is not None
    assert booking[0]["status"] == 'Booked'
    assert booking[0]["user_id"] == 6
    assert booking[0]["source"] == 'Manchester'
    
def test_listRequests(client):
    # Prepare a JSON payload for the request

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/listRequests')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    customer_requests = json.loads(response.get_data(as_text=True))
    print(customer_requests)
    #print(response.data)

    assert customer_requests[0]["status"] == 'Booked'
    assert customer_requests[0]["user_id"] == 6
    assert customer_requests[0]["source"] == 'Manchester'

def test_acceptJob(client):
    # Prepare params for the request

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/1/acceptJob?carid=3')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    jobs = json.loads(response.get_data(as_text=True))

    assert b'success' in response.data

def test_checkBooking(client):
    # Prepare a JSON payload for the request

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/checkBooking?uid=6')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    booking = json.loads(response.get_data(as_text=True))
    print(booking)

    assert booking is not None
    assert booking[0]["status"] == 'Accepted by Driver'
    assert booking[0]["user_id"] == 6
    assert booking[0]["source"] == 'Manchester'