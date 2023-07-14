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

    #Send a POST request to the createCar endpoint with the payload
    response = client.post('/api/createCar', json=payload)

    #Check that the response status code is 201 (OK)

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
   

    #Check that the car was inserted into the database

    car = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data





def test_updateCar(client):
    #Prepare a JSON payload for the request
    #TestUser ID is 7 in schema

    payload = {
                "uid": 7,
                "brand": 'Bmw',
                "model": 'M5',
                "colour": 'red',
                "next_service": '2023-06-05',
                "status": 'Booked',
        }

    #Send a POST request to the updateCar endpoint with the payload
    
    response = client.post('/api/4/updateCar', json=payload)
    

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    

    #Check that the car was inserted into the database.

    car = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data

    
def test_deleteCar(client):
    # Prepare a JSON payload for the request
    #TestUser ID is 6 in schema
    
    response = client.post('/api/4/deleteCar')

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    #Add additional assertions to validate the response data or behavior

    #Check that the car was inserted into the database

    car = json.loads(response.get_data(as_text=True))
    

    assert b'success' in response.data


def test_getCar(client):
    
    #Send a POST request to the getCar endpoint with the payload

    response = client.post('/api/3/getCar')

    #Check that the response status code is 200 (OK)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    
    #Add additional assertions to validate the response data or behavior

    #Check that the car was inserted into the database

    car = json.loads(response.get_data(as_text=True))
    print(car)
    assert car is not None
    assert car[0]["brand"] == 'Honda'
    assert car[0]["model"] == 'Civic'
    assert car[0]["user_id"] == 7