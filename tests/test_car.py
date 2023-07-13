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


def test_listCarDetails(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    response = client.post('/api/listCarDetails?uid=7')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    car = json.loads(response.get_data(as_text=True))
    print(car)

    assert car[0]["user_id"]==7
    assert car[0]["id"]==3


def test_createCar(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    payload = {
                "uid": 7,
                "brand": 'Benz',
                "model": '220',
                "colour": 'red',
                "next_service": '2023-06-05',
                "status": 'Booked',
        }

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/createCar', json=payload)

    # Check that the response status code is 201 (OK)
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    booking = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data



def test_updateCar(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    payload = {
                "uid": 7,
                "brand": 'Bmw',
                "model": 'M5',
                "colour": 'red',
                "next_service": '2023-06-05',
                "status": 'Booked',
        }

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/1/updateCar', json=payload)

    # Check that the response status code is 201 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    booking = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data

    
def test_deleteCar(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    payload = {
                "uid": 7,
                "brand": 'Bmw',
                "model": 'M5',
                "colour": 'red',
                "next_service": '2023-06-05',
                "status": 'Booked',
        }

    # Send a POST request to the bookcar endpoint with the payload
    response = client.post('/api/1/deleteCar', json=payload)

    # Check that the response status code is 201 (OK)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    # Add additional assertions to validate the response data or behavior

    # Check that the booking was inserted into the database
    booking = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data